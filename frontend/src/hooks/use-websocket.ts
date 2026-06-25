"use client"

import { useEffect, useState, useCallback, useRef } from "react"

export function useWebSocket(url: string) {
  const [lastMessage, setLastMessage] = useState<any>(null)
  const [readyState, setReadyState] = useState<number>(3) // Default to closed
  const socketRef = useRef<WebSocket | null>(null)
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null)
  const reconnectAttemptsRef = useRef(0)

  const connect = useCallback(() => {
    if (!url) return

    if (socketRef.current) {
      socketRef.current.close()
    }

    const socket = new WebSocket(url)
    socketRef.current = socket
    setReadyState(0) // Connecting

    socket.onopen = () => {
      console.log("WebSocket connected")
      setReadyState(1)
      reconnectAttemptsRef.current = 0
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current)
        reconnectTimeoutRef.current = null
      }
    }

    socket.onclose = (event) => {
      console.log("WebSocket closed", event.code, event.reason)
      setReadyState(3)
      
      // Attempt reconnection if not closed cleanly
      if (event.code !== 1000) {
        const timeout = Math.min(1000 * Math.pow(2, reconnectAttemptsRef.current), 30000)
        console.log(`Attempting reconnection in ${timeout}ms...`)
        
        reconnectTimeoutRef.current = setTimeout(() => {
          reconnectAttemptsRef.current += 1
          connect()
        }, timeout)
      }
    }

    socket.onerror = (error) => {
      console.error("WebSocket error", error)
      socket.close()
    }

    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        setLastMessage(data)
      } catch (e) {
        setLastMessage(event.data)
      }
    }
  }, [url])

  useEffect(() => {
    connect()
    return () => {
      if (socketRef.current) {
        socketRef.current.close(1000, "Component unmounted")
      }
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current)
      }
    }
  }, [connect])

  const sendMessage = useCallback((message: any) => {
    if (socketRef.current?.readyState === 1) {
      socketRef.current.send(typeof message === "string" ? message : JSON.stringify(message))
    }
  }, [])

  return { lastMessage, readyState, sendMessage }
}
