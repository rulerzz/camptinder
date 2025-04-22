This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## Getting Started

First, clone the repository:

```
git clone https://github.com/Rissukka/CampTinder.git
```

Then, install the packages. We also installed Bun, so you can use either npm or Bun:

```
npm install
```

or

```
bun install
```

If you encounter errors, try adding `--legacy-peer-deps` or `--force` after the install command.

Then, run the development server:

```
npm run dev
```

or

```
bun run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

I have set up some components from shadcn/ui that might be used in this project.

If anyone doesn't understand, you can visit the official website to read the documentation or ask me.

### Project Structure

Here's a brief explanation of the current project structure:

```
src
├── app
│   ├── [Other Routes]   # Website Routes
│   ├── globals.css      # Global styles
│   ├── layout.tsx       # Main layout file
│   ├── api              # API Routes
├── components
│   ├── navbar
│   ├── other components
│   ├── ui                # Shadcn/ui installed components
├── features              # Contains specific feature implementations
    ├── auth              # All feature/components/function for Authentication
    └── Other features    # All feature/components/function
├── lib                   # Libraries and helper functions
├── hooks                 # Reusable hooks/function
├── public
│   ├── logo.svg          # Project logo
│   └── Other public file # Project public image/file, etc...
├── Other Folder/Config   # Other configuration files
├── types                 # Type definitions
```

### How to use:

- **App**: Core application components, including layouts and global styles.
- **globals.css**: Contains styles that apply to the entire application.
- **layout.tsx**: Defines the global layout structure.
- **api**: API Routes / CRUD Function, etc...
- **components**: Reusable UI components.
- **hooks**: Reusable hooks/function
- **UI components**: Reusable UI elements from `shadcn/ui`
- **features**: Stores distinct functionality or pages.
- **lib**: Utility files, configurations, and reusable logic.
- **Public assets**: Static assets used across the app, such as images and icons.

### Notes:

- Since the project uses `NextJS`, `TypeScript`, and `ESLint`, it is very strict about case sensitivity when deploying or testing, so make sure there are no errors.
- File names should follow the kebab-case format (-), e.g., sign-in-card.tsx.

- Components from `shadcn/ui` are located in the `components/ui` folder, so don't need to create or use native HTML elements.
