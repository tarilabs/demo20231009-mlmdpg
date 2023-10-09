# Evaluate PostgreSQL Server as backend to use with ml-metadata #65

## Test 1: ml-metadata Python to PostgreSQL

Using podman compose, and `test1.py` outputs:

```
demo20231009-mlmdpg % docker exec -it e8ff94c9fc07 bash
(app-root) bash-4.4$ python test1.py 
WARNING: Logging before InitGoogleLogging() is written to STDERR
I1009 09:22:11.567962     7 postgresql_metadata_source.cc:208] Connecting to database. 
I1009 09:22:11.581920     7 postgresql_metadata_source.cc:215] Connection to database succeed.
I1009 09:22:11.626552     7 postgresql_metadata_source.cc:208] Connecting to database. 
I1009 09:22:11.630167     7 postgresql_metadata_source.cc:215] Connection to database succeed.
[id: 10
name: "DataSet"
properties {
  key: "day"
  value: INT
}
properties {
  key: "split"
  value: STRING
}
, id: 11
name: "SavedModel"
properties {
  key: "name"
  value: STRING
}
properties {
  key: "version"
  value: INT
}
]
```

As expected:

![](/screenshots/Screenshot%202023-10-09%20at%2011.26.01%20(2).png)

## Test 2: ml-metadata Python to gRPC ml-metadata server to PostgreSQL

Using podman compose, and this time `test2.py` outputs:

```
demo20231009-mlmdpg % docker ps
CONTAINER ID  IMAGE                                                  COMMAND               CREATED         STATUS                   PORTS                   NAMES
759913b5e449  gcr.io/tfx-oss-public/ml_metadata_store_server:1.14.0                        2 hours ago     Up 11 seconds            0.0.0.0:8080->8080/tcp  demo20231009-mlmdpg-mlmdserver-1
2bb711a2b659  docker.io/library/demo20231009-mlmdpg-web:latest       /bin/sh -c tail -...  22 seconds ago  Up 22 seconds                                    demo20231009-mlmdpg-web-1
b1d4d814272f  docker.io/library/postgres:12                          postgres              22 seconds ago  Up 22 seconds (healthy)  0.0.0.0:5432->5432/tcp  demo20231009-mlmdpg-pgserver-1
demo20231009-mlmdpg % docker exec -it 2bb711a2b659 bash
(app-root) bash-4.4$ python test2.py 
(app-root) bash-4.4$ 
```

As expected:

![](/screenshots/Screenshot%202023-10-09%20at%2011.35.33%20(2).png)

## Conclusions

Demonstrated PostgreSQL Server as backend to use with ml-metadata, both using direct connection as well as using the gRPC ml-metadata server.
