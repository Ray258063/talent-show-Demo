from langchain.vectorstores import InMemoryVectorStore
from langchain.docstore.document import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai import Credentials
from langchain_ibm import WatsonxLLM
from ibm_watsonx_ai.foundation_models import ModelInference

credentials = Credentials(
    url = f"https://{region}.ml.cloud.ibm.com",
    api_key = watsonx_api_key,
)

client = APIClient(credentials)

# 初始化嵌入模型
watsonx_embedding = WatsonxEmbeddings(
    model_id="intfloat/multilingual-e5-large",
    watsonx_client=client
)

# 準備文件
documents = [
    Document(page_content="Python是一種高階程式語言", metadata={"source": "programming"}),
    Document(page_content="機器學習是人工智能的重要分支", metadata={"source": "ai"})
]

# 建立並儲存向量
vectorstore = InMemoryVectorStore.from_documents(documents, watsonx_embedding)

# 儲存向量到檔案 (使用 pickle)
import pickle

with open('vector_store.pkl', 'wb') as f:
    pickle.dump(vectorstore, f)

with open('vector_store.pkl', 'rb') as f:
    loaded_vectorstore = pickle.load(f)

# 使用 as_retriever() 設定找相似前3篇
retriever = loaded_vectorstore.as_retriever(
    search_kwargs={"k": 3}
)

# 進行相似度檢索
results = retriever.invoke("程式語言")
for doc in results:
    print(doc.page_content)