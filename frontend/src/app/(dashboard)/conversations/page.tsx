"use client"

import { useState, useEffect, useRef } from "react"
import { api } from "@/lib/api"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Send, Search } from "lucide-react"
import { Skeleton } from "@/components/ui/skeleton"

interface Message {
  id: string
  content: string
  sender_type: string
  created_at: string
}

interface Conversation {
  id: string
  customer_id: string
  channel: string
  status: string
  messages: Message[]
  customer?: {
    first_name: string
    last_name: string
  }
}

export default function ConversationsPage() {
  const [conversations, setConversations] = useState<Conversation[]>([])
  const [selectedId, setSelectedId] = useState<string | null>(null)
  const [message, setMessage] = useState("")
  const [isLoading, setIsLoading] = useState(true)
  const [search, setSearch] = useState("")
  
  const scrollRef = useRef<HTMLDivElement>(null)

  const fetchConversations = async () => {
    try {
      const data = await api.get<Conversation[]>("/conversations/")
      setConversations(data)
      if (data.length > 0 && !selectedId) {
        setSelectedId(data[0].id)
      }
    } catch (err) {
      console.error("Failed to fetch conversations", err)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchConversations()
  }, [])

  useEffect(() => {
    if (scrollRef.current) {
      const scrollContainer = scrollRef.current.querySelector('[data-radix-scroll-area-viewport]');
      if (scrollContainer) {
        scrollContainer.scrollTop = scrollContainer.scrollHeight;
      }
    }
  }, [selectedId, conversations])

  const selectedConv = conversations.find((c) => c.id === selectedId)

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!message.trim() || !selectedId) return
    
    try {
      const newMessage = await api.post<Message>(`/conversations/${selectedId}/messages`, {
        content: message,
        sender_type: "AGENT",
        conversation_id: selectedId
      })
      
      setConversations(prev => prev.map(c => 
        c.id === selectedId ? { ...c, messages: [...c.messages, newMessage] } : c
      ))
      setMessage("")
    } catch (err) {
      console.error("Failed to send message", err)
    }
  }

  const filteredConversations = conversations.filter(c => 
    c.customer ? `${c.customer.first_name} ${c.customer.last_name}`.toLowerCase().includes(search.toLowerCase()) : true
  )

  return (
    <div className="flex h-[calc(100vh-64px)] overflow-hidden">
      {/* Conversation List */}
      <div className="w-80 border-r bg-muted/30 flex flex-col">
        <div className="p-4 border-b bg-background">
          <div className="relative">
            <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
            <Input 
              placeholder="Search conversations..." 
              className="h-9 pl-8" 
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>
        </div>
        <ScrollArea className="flex-1">
          {isLoading ? (
            <div className="p-4 space-y-4">
              {Array.from({ length: 5 }).map((_, i) => (
                <div key={i} className="flex items-center gap-3">
                  <Skeleton className="h-10 w-10 rounded-full" />
                  <div className="space-y-2 flex-1">
                    <Skeleton className="h-4 w-[120px]" />
                    <Skeleton className="h-3 w-full" />
                  </div>
                </div>
              ))}
            </div>
          ) : filteredConversations.length === 0 ? (
            <div className="p-4 text-center text-sm text-muted-foreground">No conversations</div>
          ) : (
            filteredConversations.map((conv) => (
              <div
                key={conv.id}
                onClick={() => setSelectedId(conv.id)}
                className={`flex items-center gap-3 p-4 cursor-pointer hover:bg-muted/50 transition-colors ${
                  selectedId === conv.id ? "bg-muted" : ""
                }`}
              >
                <Avatar>
                  <AvatarFallback>{conv.customer?.first_name?.[0] || "?"}</AvatarFallback>
                </Avatar>
                <div className="flex-1 overflow-hidden">
                  <div className="flex items-center justify-between">
                    <span className="font-semibold truncate">
                      {conv.customer ? `${conv.customer.first_name} ${conv.customer.last_name}` : "Unknown"}
                    </span>
                    <span className="text-[10px] text-muted-foreground">
                      {conv.messages.length > 0 ? new Date(conv.messages[conv.messages.length-1].created_at).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}) : ""}
                    </span>
                  </div>
                  <p className="text-sm text-muted-foreground truncate">
                    {conv.messages.length > 0 ? conv.messages[conv.messages.length-1].content : "No messages"}
                  </p>
                </div>
              </div>
            ))
          )}
        </ScrollArea>
      </div>

      {/* Chat Area */}
      <div className="flex-1 flex flex-col bg-background">
        {selectedConv ? (
          <>
            {/* Header */}
            <div className="h-16 border-b flex items-center justify-between px-6">
              <div className="flex items-center gap-3">
                <Avatar className="h-9 w-9">
                  <AvatarFallback>{selectedConv.customer?.first_name?.[0] || "?"}</AvatarFallback>
                </Avatar>
                <div>
                  <h2 className="font-semibold">
                    {selectedConv.customer ? `${selectedConv.customer.first_name} ${selectedConv.customer.last_name}` : "Unknown"}
                  </h2>
                  <div className="flex items-center gap-2">
                    <span className="text-xs text-muted-foreground">Channel: {selectedConv.channel}</span>
                    <Badge variant="outline" className="text-[10px] h-4">{selectedConv.status}</Badge>
                  </div>
                </div>
              </div>
            </div>

            {/* Messages */}
            <ScrollArea className="flex-1 p-6" ref={scrollRef}>
              <div className="flex flex-col gap-4">
                {selectedConv.messages.map((msg) => (
                  <div 
                    key={msg.id} 
                    className={`flex flex-col gap-1 ${msg.sender_type === "CUSTOMER" ? "items-start" : "items-end"}`}
                  >
                    <div 
                      className={`max-w-[70%] rounded-2xl p-3 text-sm ${
                        msg.sender_type === "CUSTOMER" 
                          ? "bg-muted text-foreground" 
                          : "bg-primary text-primary-foreground"
                      }`}
                    >
                      {msg.content}
                    </div>
                    <span className="text-[10px] text-muted-foreground px-1">
                      {new Date(msg.created_at).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                    </span>
                  </div>
                ))}
              </div>
            </ScrollArea>

            {/* Input */}
            <div className="p-4 border-t">
              <form className="flex items-center gap-2" onSubmit={handleSend}>
                <Input
                  placeholder="Type a message to take over..."
                  className="flex-1"
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                />
                <Button type="submit" size="icon" disabled={!message.trim()}>
                  <Send className="h-4 w-4" />
                </Button>
              </form>
              <p className="text-[10px] text-center mt-2 text-muted-foreground uppercase tracking-widest">
                AI Agent is currently monitoring
              </p>
            </div>
          </>
        ) : (
          <div className="flex-1 flex items-center justify-center text-muted-foreground">
            Select a conversation to start
          </div>
        )}
      </div>
    </div>
  )
}
