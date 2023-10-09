import grpc
import ml_metadata as mlmd
# import ml_metadata.metadata_store.pywrap.metadata_store_extension.metadata_store
from grpc import insecure_channel
from ml_metadata.metadata_store import metadata_store
from ml_metadata.proto import metadata_store_pb2
from ml_metadata.proto import metadata_store_service_pb2
from ml_metadata.proto import metadata_store_service_pb2_grpc

def main():
    connection_config = metadata_store_pb2.ConnectionConfig()
    connection_config.postgresql.host = 'pgserver'
    connection_config.postgresql.port = '5432'
    connection_config.postgresql.user = 'postgres'
    connection_config.postgresql.password = 'mypsw'
    connection_config.postgresql.dbname = 'pgserver'
    # connection_config.postgresql.skip_db_creation = 'false'
    # connection_config.postgresql.ssloption.sslmode = '...' # disable, allow, verify-ca, verify-full, etc.
    # connection_config.postgresql.ssloption.sslcert = '...'
    # connection_config.postgresql.ssloption.sslkey = '...'
    # connection_config.postgresql.ssloption.sslpassword = '...'
    # connection_config.postgresql.ssloption.sslrootcert = '...'
    store = metadata_store.MetadataStore(connection_config, enable_upgrade_migration=True)

    # Create ArtifactTypes, e.g., Data and Model
    data_type = metadata_store_pb2.ArtifactType()
    data_type.name = "DataSet"
    data_type.properties["day"] = metadata_store_pb2.INT
    data_type.properties["split"] = metadata_store_pb2.STRING
    data_type_id = store.put_artifact_type(data_type)

    model_type = metadata_store_pb2.ArtifactType()
    model_type.name = "SavedModel"
    model_type.properties["version"] = metadata_store_pb2.INT
    model_type.properties["name"] = metadata_store_pb2.STRING
    model_type_id = store.put_artifact_type(model_type)

    # Query all registered Artifact types.
    artifact_types = store.get_artifact_types()
    print(artifact_types)

if __name__ == '__main__':
    main()
