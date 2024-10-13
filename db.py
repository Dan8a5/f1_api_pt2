from sqlmodel import create_engine, SQLModel, Session

# Database URL
DATABASE_URL = "postgresql://postgres.shlpxirwffgjdudmxkuo:week6codeschool@aws-0-us-east-1.pooler.supabase.com:6543/postgres"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)

# Function to create all tables in SQLModel classes
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Dependency to get a database session
def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    SQLModel.metadata.create_all(engine)  # Fix capitalization of SQLModel
# Call the function to create the database and tables   
