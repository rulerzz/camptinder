import { streamText } from 'ai';
import { createOpenAI } from '@ai-sdk/openai';

// Create a custom client for MistralAI using the OpenAI-compatible API
const mistral = createOpenAI({
        apiKey: process.env.MISTRAL_API_KEY,
        baseURL: 'https://api.mistral.ai/v1',
});

export async function POST(req: Request) {
        const { messages } = await req.json();

        // Include Agent API ID in the header
        const agentApiId = process.env.MISTRAL_AGENT_API_ID;

        try {
                const result = await streamText({
                        model: mistral('mistral-small-2501'),
                        messages,
                        maxTokens: 1000,

                        headers: {
                                'X-Agent-Api-Id': agentApiId,
                        },
                });

                return result.toDataStreamResponse();
        } catch (error) {
                console.error('Error while calling Mistral API:', error);
                return new Response('Internal Server Error', { status: 500 });
        }
}
