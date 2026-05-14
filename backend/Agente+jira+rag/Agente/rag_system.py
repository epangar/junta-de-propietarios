
from elasticsearch import Elasticsearch, helpers
from sentence_transformers import SentenceTransformer
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List, Tuple, Dict, Any
import numpy as np
import os
import re
from config import Settings  # ✅ CORRECTO: importa la clase

settings = Settings()        # ✅ CORRECTO: instancia el objeto


class ElasticsearchRAGSystem:
    def __init__(self):
        self.es_client = None
        self.embedding_model = None
        self._initialize_connections()

    def _initialize_connections(self):
        """Inicializa conexiones con Elasticsearch y modelo de embeddings"""
        print("Inicializando conexiones...")
        
        if settings.ELASTICSEARCH_USER and settings.ELASTICSEARCH_PASSWORD:
            self.es_client = Elasticsearch(
                settings.ELASTICSEARCH_URL,
                basic_auth=(settings.ELASTICSEARCH_USER, settings.ELASTICSEARCH_PASSWORD),
                verify_certs=False
            )
        else:
            self.es_client = Elasticsearch(
                settings.ELASTICSEARCH_URL,
                verify_certs=False
            )
        
        if not self.es_client.ping():
            raise ConnectionError("No se pudo conectar a Elasticsearch")
        
        print(f"✓ Conectado a Elasticsearch: {settings.ELASTICSEARCH_URL}")
        
        self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)
        print(f"✓ Modelo de embeddings cargado: {settings.EMBEDDING_MODEL}")

    def _create_index(self):
        """Crea el índice en Elasticsearch con mapping para vectores"""
        index_mapping = {
            "mappings": {
                "properties": {
                    "content": {
                        "type": "text",
                        "analyzer": "standard"
                    },
                    "embedding": {
                        "type": "dense_vector",
                        "dims": settings.EMBEDDING_DIMENSION,
                        "index": True,
                        "similarity": "cosine"
                    },
                    "metadata": {
                        "type": "object",
                        "enabled": True
                    },
                    "chunk_id": {
                        "type": "keyword"
                    }
                }
            },
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            }
        }
        
        if self.es_client.indices.exists(index=settings.ELASTICSEARCH_INDEX):
            self.es_client.indices.delete(index=settings.ELASTICSEARCH_INDEX)
            print(f"Índice existente eliminado: {settings.ELASTICSEARCH_INDEX}")
        
        self.es_client.indices.create(
            index=settings.ELASTICSEARCH_INDEX,
            body=index_mapping
        )
        print(f"✓ Índice creado: {settings.ELASTICSEARCH_INDEX}")

    def load_documents(self, docs_path: str = None) -> List[Document]:
        """Carga documentos desde un directorio (txt, md, pdf)"""
        if docs_path is None:
            docs_path = settings.DOCS_PATH
        
        print(f"Cargando documentos desde {docs_path}...")
        
        if not os.path.exists(docs_path):
            raise FileNotFoundError(f"El directorio {docs_path} no existe")
        
        documents = []
        
        txt_loader = DirectoryLoader(
            docs_path,
            glob="**/*.txt",
            loader_cls=TextLoader,
            show_progress=True
        )
        try:
            documents.extend(txt_loader.load())
        except Exception as e:
            print(f"Advertencia al cargar archivos .txt: {e}")
        
        md_loader = DirectoryLoader(
            docs_path,
            glob="**/*.md",
            loader_cls=TextLoader,
            show_progress=True
        )
        try:
            documents.extend(md_loader.load())
        except Exception as e:
            print(f"Advertencia al cargar archivos .md: {e}")
        
        pdf_loader = DirectoryLoader(
            docs_path,
            glob="**/*.pdf",
            loader_cls=PyPDFLoader,
            show_progress=True
        )
        try:
            documents.extend(pdf_loader.load())
        except Exception as e:
            print(f"Advertencia al cargar archivos .pdf: {e}")
        
        print(f"✓ Cargados {len(documents)} documentos")
        return documents

    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """Divide documentos en fragmentos con solapamiento"""
        print("Dividiendo documentos en chunks...")
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            separators=["\n\n", "\n", ". ", " ", ""],
            length_function=len
        )
        
        chunks = text_splitter.split_documents(documents)
        print(f"✓ Generados {len(chunks)} chunks con solapamiento de {settings.CHUNK_OVERLAP} caracteres")
        
        return chunks

    def index_documents(self, docs_path: str = None):
        """Pipeline completo de indexación en Elasticsearch"""
        self._create_index()
        
        documents = self.load_documents(docs_path)
        
        if not documents:
            raise ValueError("No se encontraron documentos para indexar")
        
        chunks = self.chunk_documents(documents)
        
        print("Generando embeddings e indexando en Elasticsearch...")
        
        actions = []
        batch_size = 100
        
        for i, chunk in enumerate(chunks):
            embedding = self.embedding_model.encode(
                chunk.page_content,
                normalize_embeddings=True
            )
            
            doc = {
                "_index": settings.ELASTICSEARCH_INDEX,
                "_id": f"chunk_{i}",
                "_source": {
                    "content": chunk.page_content,
                    "embedding": embedding.tolist(),
                    "metadata": chunk.metadata,
                    "chunk_id": f"chunk_{i}"
                }
            }
            
            actions.append(doc)
            
            if len(actions) >= batch_size:
                helpers.bulk(self.es_client, actions)
                print(f"Indexados {i + 1}/{len(chunks)} chunks")
                actions = []
        
        if actions:
            helpers.bulk(self.es_client, actions)
        
        self.es_client.indices.refresh(index=settings.ELASTICSEARCH_INDEX)
        
        print(f"✓ Indexación completada: {len(chunks)} chunks indexados")

    def search_similar(
        self,
        query: str,
        k: int = None
    ) -> List[Dict[str, Any]]:
        """Búsqueda por similitud vectorial en Elasticsearch"""
        if k is None:
            k = settings.K_INITIAL
        
        query_embedding = self.embedding_model.encode(
            query,
            normalize_embeddings=True
        )
        
        search_query = {
            "query": {
                "script_score": {
                    "query": {"match_all": {}},
                    "script": {
                        "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                        "params": {"query_vector": query_embedding.tolist()}
                    }
                }
            },
            "_source": ["content", "metadata", "chunk_id"],
            "size": k
        }
        
        response = self.es_client.search(
            index=settings.ELASTICSEARCH_INDEX,
            body=search_query
        )
        
        results = []
        for hit in response['hits']['hits']:
            results.append({
                'content': hit['_source']['content'],
                'metadata': hit['_source']['metadata'],
                'chunk_id': hit['_source']['chunk_id'],
                'score': hit['_score']
            })
        
        return results

    def search_with_reranking(
        self,
        query: str,
        k_initial: int = None,
        k_final: int = None
    ) -> Tuple[List[Dict[str, Any]], np.ndarray]:
        """Búsqueda con reranking basado en scores de Elasticsearch"""
        if k_initial is None:
            k_initial = settings.K_INITIAL
        if k_final is None:
            k_final = settings.K_FINAL
        
        initial_results = self.search_similar(query, k=k_initial)
        
        if not initial_results:
            return [], np.array([])
        
        scores = np.array([result['score'] for result in initial_results])
        
        final_results = initial_results[:k_final]
        final_scores = scores[:k_final]
        
        return final_results, final_scores

    def query(self, question: str, k: int = None) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Método principal para consultar el sistema RAG
        
        Args:
            question: Pregunta del usuario
            k: Número de documentos finales a retornar
            
        Returns:
            tuple: (respuesta_generada, lista_de_fuentes)
        """
        if k is None:
            k = settings.K_FINAL
        
        try:
            results, scores = self.search_with_reranking(
                query=question,
                k_initial=settings.K_INITIAL,
                k_final=k
            )
            
            if not results:
                return "No se encontraron documentos relevantes para responder tu pregunta.", []
            
            context_parts = []
            for i, result in enumerate(results, 1):
                context_parts.append(f"[Fragmento {i}]\n{result['content']}")
            
            context = "\n\n".join(context_parts)
            
            answer = self._generate_llm_response(question, context, results)
            
            sources = []
            for result in results:
                sources.append({
                    "content": result['content'][:300] + "..." if len(result['content']) > 300 else result['content'],
                    "metadata": {
                        **result['metadata'],
                        "chunk_id": result['chunk_id'],
                        "relevance_score": float(result['score'])
                    }
                })
            
            return answer, sources
            
        except Exception as e:
            raise Exception(f"Error en query: {str(e)}")

    def _generate_llm_response(self, question: str, context: str, results: List[Dict]) -> str:
        """Genera respuesta inteligente basada en el contexto"""
        try:
            if hasattr(settings, 'LLM_MODEL') and settings.LLM_MODEL.startswith("ollama/"):
                try:
                    prompt = f"""Responde en ESPAÑOL de forma clara y directa.

Contexto:
{context[:2000]}

Pregunta: {question}

Instrucciones:
- Responde SOLO con la información específica que responde la pregunta
- Sé breve y directo
- Cita el artículo o sección relevante

Respuesta:"""
                    return self._call_ollama(prompt)
                except Exception as ollama_error:
                    print(f"⚠️ Ollama falló: {ollama_error}")
                    print("Usando respuesta inteligente del contexto...")
                    return self._extract_smart_answer(question, context, results)
            
            elif hasattr(settings, 'OPENAI_API_KEY') and settings.OPENAI_API_KEY:
                prompt = f"""Responde en ESPAÑOL de forma clara y directa.

Contexto:
{context[:2000]}

Pregunta: {question}

Respuesta:"""
                return self._call_openai(prompt)
            
            else:
                return self._extract_smart_answer(question, context, results)
                
        except Exception as e:
            raise Exception(f"Error generando respuesta: {str(e)}")

    def _extract_smart_answer(self, question: str, context: str, results: List[Dict]) -> str:
        """Extrae respuesta inteligente del contexto sin LLM"""
        
        question_lower = question.lower()
        
        topic_keywords = {
            'piscina': ['piscina', 'nadar', 'bañar'],
            'ruido': ['ruido', 'sonido', 'volumen', 'música'],
            'obra': ['obra', 'reforma', 'construcción', 'reparación'],
            'basura': ['basura', 'residuo', 'reciclaje'],
            'mascota': ['mascota', 'perro', 'gato', 'animal'],
            'garaje': ['garaje', 'parking', 'estacionamiento', 'plaza'],
            'jardin': ['jardín', 'zona verde', 'planta']
        }
        
        detected_topic = None
        for topic, keywords in topic_keywords.items():
            if any(keyword in question_lower for keyword in keywords):
                detected_topic = topic
                break
        
        relevant_article = None
        relevant_content = None
        
        for result in results:
            content = result['content']
            content_lower = content.lower()
            
            if detected_topic:
                topic_keywords_list = topic_keywords[detected_topic]
                if any(keyword in content_lower for keyword in topic_keywords_list):
                    article_match = re.search(r'Artículo\s+(\d+)[^\n]*', content)
                    if article_match:
                        relevant_article = article_match.group(0)
                        relevant_content = content
                        break
        
        if not relevant_content:
            relevant_content = results[0]['content']
            article_match = re.search(r'Artículo\s+\d+[^\n]*', relevant_content)
            if article_match:
                relevant_article = article_match.group(0)
        
        if detected_topic == 'piscina':
            return self._format_piscina_answer(relevant_content, relevant_article)
        elif detected_topic == 'ruido':
            return self._format_ruido_answer(relevant_content, relevant_article)
        elif detected_topic == 'obra':
            return self._format_obra_answer(relevant_content, relevant_article)
        else:
            return self._format_generic_answer(relevant_content, relevant_article, question)

    def _format_piscina_answer(self, content: str, article: str) -> str:
        response = "**Según la normativa de la comunidad:**\n\n"
        horario_match = re.search(r'Horario de uso:\s*(\d{1,2}:\d{2})\s*a\s*(\d{1,2}:\d{2})', content)
        if horario_match:
            response += f"• **Horario de uso de la piscina: {horario_match.group(1)} a {horario_match.group(2)} horas.**\n\n"
        normas = []
        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('•') and 'piscina' in line.lower():
                normas.append(line)
        if normas:
            response += "**Normas adicionales:**\n"
            for norma in normas[:3]:
                response += f"{norma}\n"
        if article:
            response += f"\n*Fuente: {article}*"
        return response

    def _format_ruido_answer(self, content: str, article: str) -> str:
        response = "**Según la normativa de la comunidad:**\n\n"
        horario_match = re.search(r'ruidos.*?(\d{1,2}:\d{2})\s*y\s*(?:las\s*)?(\d{1,2}:\d{2})', content, re.IGNORECASE)
        if horario_match:
            response += f"• **No se permitirán ruidos excesivos entre las {horario_match.group(1)} y las {horario_match.group(2)} horas.**\n\n"
        normas = []
        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('•') and any(word in line.lower() for word in ['celebracion', 'música', 'voces', 'volumen']):
                normas.append(line)
        if normas:
            response += "**Detalles adicionales:**\n"
            for norma in normas[:2]:
                response += f"{norma}\n"
        if article:
            response += f"\n*Fuente: {article}*"
        return response

    def _format_obra_answer(self, content: str, article: str) -> str:
        response = "**Según la normativa de la comunidad:**\n\n"
        horarios = []
        for line in content.split('\n'):
            line = line.strip()
            if 'lunes' in line.lower() or 'sábado' in line.lower() or 'domingo' in line.lower():
                if re.search(r'\d{1,2}:\d{2}', line):
                    horarios.append(line)
        if horarios:
            response += "**Horarios permitidos para obras:**\n"
            for horario in horarios[:3]:
                response += f"{horario}\n"
        if article:
            response += f"\n*Fuente: {article}*"
        return response

    def _format_generic_answer(self, content: str, article: str, question: str) -> str:
        response = "**Según la normativa de la comunidad:**\n\n"
        sentences = []
        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('•') and len(line) > 20:
                sentences.append(line)
        for sentence in sentences[:3]:
            response += f"{sentence}\n"
        if article:
            response += f"\n*Fuente: {article}*"
        return response

    def _call_ollama(self, prompt: str) -> str:
        """Llama a Ollama para generar respuesta con timeout extendido"""
        try:
            import requests
            
            model_name = settings.LLM_MODEL.replace("ollama/", "")
            
            if len(prompt) > 3000:
                prompt = prompt[:3000] + "\n\n[Contexto truncado]\n\nResponde basándote en la información anterior."
            
            response = requests.post(
                f"{settings.OLLAMA_BASE_URL}/api/generate",
                json={
                    "model": model_name,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_predict": 300,
                        "temperature": 0.3
                    }
                },
                timeout=300
            )
            
            if response.status_code == 200:
                return response.json()["response"]
            else:
                raise Exception(f"Error en Ollama: {response.status_code}")
                
        except requests.exceptions.Timeout:
            raise Exception("Timeout: Ollama tardó demasiado en responder")
        except Exception as e:
            raise Exception(f"Error llamando a Ollama: {str(e)}")

    def _call_openai(self, prompt: str) -> str:
        """Llama a OpenAI para generar respuesta"""
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=settings.OPENAI_API_KEY)
            
            response = client.chat.completions.create(
                model=settings.LLM_MODEL,
                messages=[
                    {"role": "system", "content": "Eres un asistente especializado en responder preguntas sobre normativas de comunidades de propietarios. SIEMPRE respondes en ESPAÑOL de forma clara y directa."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=300
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"Error llamando a OpenAI: {str(e)}")

    def get_index_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas del índice"""
        try:
            stats = self.es_client.indices.stats(index=settings.ELASTICSEARCH_INDEX)
            count = self.es_client.count(index=settings.ELASTICSEARCH_INDEX)
            
            return {
                "index_name": settings.ELASTICSEARCH_INDEX,
                "document_count": count['count'],
                "size_in_bytes": stats['_all']['total']['store']['size_in_bytes'],
                "size_human": stats['_all']['total']['store']['size']
            }
        except Exception as e:
            return {
                "error": str(e),
                "message": "No se pudieron obtener estadísticas del índice"
            }


def initialize_rag_system(force_reindex: bool = False) -> ElasticsearchRAGSystem:
    """Inicializa el sistema RAG con Elasticsearch"""
    rag = ElasticsearchRAGSystem()
    
    index_exists = rag.es_client.indices.exists(index=settings.ELASTICSEARCH_INDEX)
    
    if not index_exists or force_reindex:
        print("Indexando documentos en Elasticsearch...")
        rag.index_documents()
    else:
        print(f"✓ Usando índice existente: {settings.ELASTICSEARCH_INDEX}")
    
    return rag
