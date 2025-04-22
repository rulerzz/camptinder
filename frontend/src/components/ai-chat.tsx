'use client';

import type React from 'react';
import { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Sparkles, Loader2 } from 'lucide-react';
import { useChat } from '@ai-sdk/react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { cn } from '@/utils/utils';

export default function AIChat() {
        const [suggestions, setSuggestions] = useState<string[]>([]);
        const inputRef = useRef<HTMLInputElement>(null);
        const chatContainerRef = useRef<HTMLDivElement>(null);
        const [autoScroll, setAutoScroll] = useState(true);
        const [showSuggestions, setShowSuggestions] = useState(true);

        const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat({
                api: '/api/chat',
        });

        useEffect(() => {
                // Fetch suggestions
                fetch('/api/chat/suggestions')
                        .then((res) => res.json())
                        .then((data) => setSuggestions(data.suggestions))
                        .catch((err) => console.error('Failed to load suggestions:', err));
        }, []);

        const handleSuggestionClick = (suggestion: string) => {
                if (inputRef.current) {
                        inputRef.current.value = suggestion;
                        handleInputChange({ target: inputRef.current } as React.ChangeEvent<HTMLInputElement>);

                        // Submit the form with the suggestion
                        const form = inputRef.current.form;
                        if (form) {
                                const submitEvent = new Event('submit', { cancelable: true, bubbles: true });
                                form.dispatchEvent(submitEvent);
                        }
                }
        };

        // Handle manual scrolling detection
        const handleScroll = () => {
                if (!chatContainerRef.current) return;

                const { scrollTop, scrollHeight, clientHeight } = chatContainerRef.current;
                // If user scrolls up more than 100px from bottom, disable auto-scroll
                const isScrolledUp = scrollHeight - scrollTop - clientHeight > 100;
                setAutoScroll(!isScrolledUp);
        };

        // Auto-scroll to bottom when new messages arrive, but only if autoScroll is true
        useEffect(() => {
                if (chatContainerRef.current && autoScroll) {
                        // Only scroll to bottom when a new message is added or when loading state changes
                        chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
                }
        }, [messages, isLoading, autoScroll]);

        // Track when to show suggestions
        useEffect(() => {
                console.log(messages);
                if (messages.length > 0) {
                        // Hide suggestions when user sends a message or when AI is typing
                        if (messages[messages.length - 1].role === 'user' || isLoading) {
                                setShowSuggestions(false);
                        }
                        // Show suggestions after AI responds
                        else if (messages[messages.length - 1].role === 'assistant' && !isLoading) {
                                setShowSuggestions(true);
                        }
                }
        }, [messages, isLoading]);

        // Re-enable auto-scroll when user sends a new message
        useEffect(() => {
                if (messages.length > 0 && messages[messages.length - 1].role === 'user') {
                        setAutoScroll(true);
                }
        }, [messages]);
        const formatMessageContent = (content: string) => {
                // Remove ### và **, and replace (\n) to <br />
                return content
                        .replace(/(#{1,6}|\*{1,3})/g, '') // Remove ### and ***
                        .split('\n') // Split by new line
                        .map((line, index, array) => (
                                <span key={index}>
                                        {line}
                                        {index < array.length - 1 && <br />}{' '}
                                        {/* Add <br /> if it's not the last line */}
                                </span>
                        ));
        };
        // Group messages by sender with suggestions after each AI message
        const renderMessages = () => {
                const messageElements: JSX.Element[] = [];

                for (let i = 0; i < messages.length; i++) {
                        const message = messages[i];
                        const formattedMessage = formatMessageContent(message.content);
                        // Add the message
                        messageElements.push(
                                <div
                                        key={message.id}
                                        className={cn(
                                                'flex items-start gap-3 text-sm',
                                                message.role === 'user' ? 'justify-end' : 'justify-start',
                                        )}
                                >
                                        {message.role !== 'user' && (
                                                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-700 flex items-center justify-center">
                                                        <Bot className="h-4 w-4 text-primary" />
                                                </div>
                                        )}

                                        <div
                                                className={cn(
                                                        'rounded-lg px-3 py-2 max-w-[80%] break-words',
                                                        message.role === 'user'
                                                                ? 'bg-primary text-white'
                                                                : 'bg-gray-700 text-gray-100',
                                                )}
                                        >
                                                {formattedMessage}
                                        </div>

                                        {message.role === 'user' && (
                                                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-primary flex items-center justify-center">
                                                        <User className="h-4 w-4 text-white" />
                                                </div>
                                        )}
                                </div>,
                        );

                        // Add suggestions after AI messages if it's the last message or followed by a user message
                        if (
                                message.role === 'assistant' &&
                                showSuggestions &&
                                i === messages.length - 1 &&
                                !isLoading
                        ) {
                                messageElements.push(
                                        <div key={`suggestions-${i}`} className="mt-3 mb-2">
                                                <div className="overflow-x-auto pb-2">
                                                        <div className="flex gap-2 w-max">
                                                                {suggestions.map((suggestion, index) => (
                                                                        <Button
                                                                                key={index}
                                                                                variant="outline"
                                                                                size="sm"
                                                                                className="text-xs whitespace-nowrap bg-gray-700 border-gray-600 hover:bg-gray-600 text-gray-200"
                                                                                onClick={() =>
                                                                                        handleSuggestionClick(
                                                                                                suggestion,
                                                                                        )
                                                                                }
                                                                        >
                                                                                {suggestion}
                                                                        </Button>
                                                                ))}
                                                        </div>
                                                </div>
                                        </div>,
                                );
                        }
                }

                return messageElements;
        };

        return (
                <Card className="border-0 bg-gray-800 text-white shadow-lg flex flex-col  max-h-[600px] overflow-hidden">
                        <CardHeader className="pb-2 pt-4 px-4 border-b border-gray-700 flex-shrink-0">
                                <CardTitle className="text-sm flex items-center gap-2">
                                        <Sparkles className="h-4 w-4 text-primary" />
                                        Camptinder.com Assistant
                                </CardTitle>
                        </CardHeader>

                        <CardContent className="p-0 flex-1 overflow-y-auto">
                                {messages.length === 0 ? (
                                        <div className="p-4 h-full flex flex-col justify-center items-center text-center space-y-4 overflow-y-auto">
                                                <div className="bg-gray-700 rounded-full p-3">
                                                        <Bot className="h-6 w-6 text-primary" />
                                                </div>
                                                <div className="space-y-2">
                                                        <h3 className="text-sm font-medium">
                                                                How can I help you today?
                                                        </h3>
                                                        <p className="text-xs text-gray-400">
                                                                Ask me anything about your camping needs.
                                                        </p>
                                                </div>

                                                <div className="w-full space-y-2 mt-4">
                                                        <p className="text-xs text-gray-400">Try asking</p>
                                                        <div className="flex flex-wrap gap-2 justify-center">
                                                                {suggestions.map((suggestion, index) => (
                                                                        <Button
                                                                                key={index}
                                                                                variant="outline"
                                                                                size="sm"
                                                                                className="text-xs bg-gray-700 border-gray-600 hover:bg-gray-600 text-gray-200"
                                                                                onClick={() =>
                                                                                        handleSuggestionClick(
                                                                                                suggestion,
                                                                                        )
                                                                                }
                                                                        >
                                                                                {suggestion}
                                                                        </Button>
                                                                ))}
                                                        </div>
                                                </div>
                                        </div>
                                ) : (
                                        <div
                                                ref={chatContainerRef}
                                                className="h-full overflow-y-auto p-4 space-y-4 scroll-smooth"
                                                onScroll={handleScroll}
                                        >
                                                {renderMessages()}

                                                {isLoading && (
                                                        <div className="flex items-start gap-3 text-sm">
                                                                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-700 flex items-center justify-center">
                                                                        <Bot className="h-4 w-4 text-primary" />
                                                                </div>
                                                                <div className="bg-gray-700 rounded-lg px-3 py-2 text-gray-100">
                                                                        <div className="flex space-x-1">
                                                                                <div className="w-2 h-2 rounded-full bg-gray-400 animate-pulse"></div>
                                                                                <div className="w-2 h-2 rounded-full bg-gray-400 animate-pulse delay-150"></div>
                                                                                <div className="w-2 h-2 rounded-full bg-gray-400 animate-pulse delay-300"></div>
                                                                        </div>
                                                                </div>
                                                        </div>
                                                )}
                                        </div>
                                )}
                        </CardContent>

                        <CardFooter className="p-3 border-t border-gray-700 flex-shrink-0">
                                <form onSubmit={handleSubmit} className="flex w-full gap-2">
                                        <Input
                                                ref={inputRef}
                                                type="text"
                                                value={input}
                                                onChange={handleInputChange}
                                                placeholder="Message Camptinder.com Assistant..."
                                                className="flex-1 bg-gray-700 border-gray-600 text-white placeholder:text-gray-400 focus-visible:ring-primary"
                                                disabled={isLoading}
                                        />
                                        <Button
                                                type="submit"
                                                disabled={isLoading}
                                                className="bg-primary hover:bg-primary/80 text-white h-10 px-3 aspect-square"
                                        >
                                                {isLoading ? (
                                                        <Loader2 className="h-4 w-4 animate-spin" />
                                                ) : (
                                                        <Send className="h-4 w-4" />
                                                )}
                                                <span className="sr-only">Send message</span>
                                        </Button>
                                </form>
                        </CardFooter>
                </Card>
        );
}
