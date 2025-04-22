import { NextResponse } from 'next/server';

export async function GET() {
        // Add suggestions about camping / firewood / pellets / liquids / camping equipment
        const suggestions = [
                'How to buy firewood?',
                'How to rent camping equipment?',
                'How to pack a camping backpack efficiently?',
                'Where to find the best camping spots?',
                'How to choose the right tent for camping?',
                'How to start a campfire safely?',
                'How to store firewood properly?',
                'What camping equipment do I need for a weekend trip?',
                'How to clean and maintain camping gear?',
        ];

        return NextResponse.json({ suggestions });
}
