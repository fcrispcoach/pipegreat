import os
import sys
import logging
from datetime import datetime
from great_expectations.data_context import DataContext


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


GE_ROOT_DIR = os.path.join(os.path.dirname(__file__), "..")
DATA_DIR = os.path.join(GE_ROOT_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

def validate_data(csv_file_path: str = None):
    """
    Valida dados usando Great Expectations.
    
    Args:
        csv_file_path (str, optional): Caminho absoluto para o arquivo CSV.
                                      Se None, usa padrão baseado na data.
    Returns:
        dict: Resultados da validação
    """
    try:
        
        today = datetime.now().strftime('%Y%m%d')
        csv_file = csv_file_path or os.path.join(DATA_DIR, "processed", f"customers_{today}.csv")
        
        logger.info(f"Iniciando validação para o arquivo: {csv_file}")
        
        
        context = DataContext(context_root_dir=os.path.join(GE_ROOT_DIR, "great_expectations"))
        
        
        batch_request = {
            "datasource_name": "my_datasource",
            "data_connector_name": "default_runtime_data_connector_name",
            "data_asset_name": "my_runtime_asset_name",
            "runtime_parameters": {"path": os.path.abspath(csv_file)},
            "batch_identifiers": {
                "runtime_batch_identifier_name": "default_identifier"
            },
        }

        
        checkpoint = context.add_or_update_checkpoint(
            name="customer_checkpoint",
            class_name="SimpleCheckpoint",
            validations=[{
                "batch_request": batch_request,
                "expectation_suite_name": "suitege",
            }],
        )

        
        results = checkpoint.run()
        context.build_data_docs()
        
        docs_path = os.path.join(
            context.root_directory,
            "uncommitted/data_docs/local_site/index.html"
        )
        
        logger.info(f"Validação concluída com sucesso! Relatório em: {docs_path}")
        return {
            "status": "success",
            "results": results,
            "data_docs": docs_path
        }

    except Exception as e:
        logger.error(f"Falha na validação: {str(e)}", exc_info=True)
        return {
            "status": "failed",
            "error": str(e)
        }

if __name__ == "__main__":
    try:
        
        csv_file = sys.argv[1] if len(sys.argv) > 1 else None
        
        result = validate_data(csv_file)
        
        if result["status"] == "success":
            print("✅ Validação concluída com sucesso!")
            print(f"📊 Relatório disponível em: file://{result['data_docs']}")
            sys.exit(0)
        else:
            print(f"❌ Falha na validação: {result['error']}")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Erro crítico: {str(e)}")
        sys.exit(1)