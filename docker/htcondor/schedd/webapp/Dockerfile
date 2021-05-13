FROM golang:1.16
WORKDIR /go/src/github.com/dodasts/schedd-app/
COPY main.go .
RUN go mod init github.com/dodasts/schedd-app && go mod tidy && CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o app .
