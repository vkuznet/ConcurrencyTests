package main

// Author: Valentin Kuznetsov < vkuznet AT gmail DOT com >
// Simple HTTP server to serve static content, i.e. Hello World example

import "net/http"

func defaultHandler(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusOK)
	w.Write([]byte("Hello from Go"))
}

func main() {
	http.HandleFunc("/", defaultHandler)
	server := &http.Server{
		Addr: ":8212",
	}
	server.ListenAndServe()
}
