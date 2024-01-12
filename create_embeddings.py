
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores.faiss import FAISS
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader

# Setting path for input data files
DATA_PATH = 'data/'

# Path for vectorstore to store text embeddings made from the data
DB_FAISS_PATH = 'vectorstore/db_faiss'

# Create vector database
def create_vector_db():

    # Load the PDF documents
    loader = DirectoryLoader(DATA_PATH,
                             glob='*.pdf',
                             loader_cls=PyPDFLoader)

    documents = loader.load()
    
    print(len(documents))
    
    # Split the text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512,
                                                   chunk_overlap=64)
    texts = text_splitter.split_documents(documents)

    # Using hugging face embeddings
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    
    # Converting all the chunks into text embeddings (Converting text into vectors)
    # After text is converted into vectors, it can be used to many task like classifications etc.
    db = FAISS.from_documents(texts, embeddings)
    
    # Saving the embeddings in the vector store
    db.save_local(DB_FAISS_PATH)

if __name__ == "__main__":
    create_vector_db()