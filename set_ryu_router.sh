#!/bin/bash
# setting ip addresses
curl -X POST -d '{"address":"192.168.1.254/24"}' http://localhost:8080/router/0000000000000001
curl -X POST -d '{"address":"192.168.2.254/24"}' http://localhost:8080/router/0000000000000003
curl -X POST -d '{"address":"192.168.3.254/24"}' http://localhost:8080/router/0000000000000003
curl -X POST -d '{"address":"10.0.0.1/8"}' http://localhost:8080/router/0000000000000001
curl -X POST -d '{"address":"10.0.0.2/8"}' http://localhost:8080/router/0000000000000003

#setting default routes
curl -X POST -d '{"gateway":"10.0.0.2"}' http://localhost:8080/router/0000000000000001
curl -X POST -d '{"gateway":"10.0.0.1"}' http://localhost:8080/router/0000000000000003

# setting static routes
curl -X POST -d '{"destination":"192.168.2.0/24","gateway":"10.0.0.2"}' http://localhost:8080/router/0000000000000001
curl -X POST -d '{"destination":"192.168.3.0/24","gateway":"10.0.0.2"}' http://localhost:8080/router/0000000000000001
curl -X POST -d '{"destination":"192.168.1.0/24","gateway":"10.0.0.1"}' http://localhost:8080/router/0000000000000003
