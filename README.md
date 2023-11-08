# Moleserv

Moleserv is a server framework for the [*Molerat*](https://molerat.trinket.icu) protocol. It features a simple syntax for building complicated servers that conform to the [Molerat](https://molerat.trinket.icu) protocol.

## Install

```bash
pip install moleserv
```

## Use

### Basic example

```py
from moleserv.server import Server

server = Server("127.0.0.1")
    .get("/", get_index)
    .get("/about", get_about)

    .put("/", put_index)
    .put("/login", put_login)

server.listen("key.pem", "cert.pem")
```

The server class takes in an address and an optional port (the default is `2693`)

### Adding routes

To add a route to `moleserv` call the function that is the method you wish to use.

Supported methods are 

- `get`
- `put`
- `del` note that the function for `del` is actually `delete` since `del` is reserved in Python.

The function takes in a path and a handler function.

For example, to create a path to serve the index page, you would do this:

```py
server.get("/", index_handler)
```

Or, to serve the about page;

```py
server.get("/about", about_handler)
```

The same path can be specified for different methods:

```py
server.get("/", get_index_handler)
      .put("/", put_index_handler)
```

### The handler function

Every route must have a handler function. When a client requests that route, Moleserv will call that function to get the response to send to the client.

A handler function is expected to take in one argument that is the client request, and return one variable that is the response.

Here is an example handler function:

```py
def handle_get_index(req: Request) -> Response:
    return Response(10, "Success", content_type="text/plain", content="hello, world!")
```

And the corresponding path specifier:

```py
server.get("/", handle_get_index)
```

### Requests

The request class holds all the data from the client's request to the server.

#### Create a Request

```py
req = Request(data) 
```

Initializing a Request with data will automatically parse and populate the class.

#### Request method

```py
req.kind
```

One of the enum `moleserv.request.RequestMethod`. 

```py
class RequestMethod(Enum):
    GET=0
    PUT=1
    DEL=2
```

This corresponds to the method used in the request.

#### Request length

```py
req.length
```

This refers the content-length of the request. It is used internally to ensure that the entire request is received. It can be used to easily get the encoded length of the `req.keys`.

#### Request hash

```py
req.hash
```

The Request hash is the client-provided ID for the `req.keys`. It should be a sha256sum of the keys, but there are no guarantees.

#### Request keys

```py
req.keys
```

These are the parsed key-values sent by the client. For example, if the request looked like this:

```plain
put example.com/login
length:32
hash:02f53083ac99d85db16d2226b370c8137e6d2f4f8a5a52dad84d12d6a9f6f471

username:potat
password:molerat
```

Then the `req.keys` would look like this:

```py
req.keys = {
        "username": "potat",
        "password": "molerat"
    }
```

They can be used to access data sent by the client.

### Responses

The Response class holds data that can be encoded into a valid `molerat` response.

#### Initializing a Response

```py
res = Response(
        status=10,
        message="Success",
        content_type="text/molerat",
        content="# Hello, world!"
    )
```

Where

- `status` is the response code of the Response.
- `message` is the optional status message of the response.
- `content_type` is the content MIME Type of the response. The default is `text/molerat`
- `content` is the text content to be sent with the response.

For error responses, content is not required. Here is an example of a minimal not-found response:

```py
res = Response(32, "Not found")
```

#### Displaying a Response

Calling `stringify()` on Response will render it as a sendable response.

For example:

```py
print(Response(10, "Success", content="# Hello, world!"))
```

Would print this:

```bash
$ python app.py
10
message:Success	
type:text/molerat	
length:15	
hash:55ae6348e27e47214b28bea4d91d7f21914be30faf77af996859b24a73339230	


# Hello, world!
```

### Starting the server

Once you've added all your routes to the server you can start it by calling `server.listen("path/to/keyfile", "path/to/certificate")`

## Contributing

This repository is mainly hosted at [git.trinket.icu/moleserv.git](https://git.trinket.icu/moleserv.git), so email patches to moleserv@git.trinket.icu are preferred. However, pull requests to the Github repository are also perfectly acceptable. Also feel free to create issues on the Github repository.
