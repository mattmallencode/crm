import pytest
from application import application
from dotenv import load_dotenv
load_dotenv
import os 

@pytest.fixture
def client():
    """Configures the app for testing

    Sets app config variable ``TESTING`` to ``True``

    :return: App for testing
    """

    #application.config['TESTING'] = True
    client = application.test_client()

    yield client

'''@pytest.fixture()
async def init_db():
    conn = await db.set_bind(os.getenv('DB_HOST'))
    yield conn

    await conn.close()'''