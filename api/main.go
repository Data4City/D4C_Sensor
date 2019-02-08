package main

import (
	"github.com/gin-gonic/gin"
)

func main() {
	router := gin.Default()
	sensors := new(Fuck.Sensor)
	api := router.Group("/api")
	{
		api.GET("/", sensors.GetValues)
	}

	router.Run()
}
