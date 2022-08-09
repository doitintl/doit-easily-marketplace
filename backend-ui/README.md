# Backend Integration - UI

This is a User Interface for the backend integration API. 

## Environment Variables

|Variable Name|Platform|Description|  Example|
|--|--|---|--|
|PORT|GKE|The port the container should run on |8080|
|API_URL|GKE|The URL for the backend integration API|http://doit-easily-api.prod.svc.cluster.local:8080|
|URL_PREFIX|GKE|The prefix to append to all routes, should match path rules in your ingress|/be|
