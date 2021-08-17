FROM golang:1.16
WORKDIR /go/src/github.com/dodasts/schedd-app/

COPY main.go .
COPY go.mod .
COPY go.sum .

RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o app .
