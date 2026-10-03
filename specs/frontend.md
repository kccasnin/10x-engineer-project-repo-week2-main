# Frontend Specification for PromptLab

This document outlines the frontend architecture, screen requirements, component inventory, state management, and UI state behaviors for the PromptLab application, based on the provided backend API and project guidelines.

The PromptLab frontend is a React-based user interface for managing prompts and their associated collections and tags.

The frontend will communicate with the existing PromptLab FastAPI backend through its REST API. The frontend will provide users with the ability to view, search, create, update, and delete prompts, as well as view and manage collections and tags supported by the backend API.

## 1. Screens and Their Purposes

1.  **Dashboard Screen**: 
    *   **Purpose**: Serves as the landing page, providing a high-level overview of the application by displaying the total count of prompts, collections, and recent activity.

    **Primary functionality:**

        - Display the total number of prompts.
        - Display the total number of collections.
        - Display recent prompt and collection activity.
        - Provide navigation to the Prompt List Screen.
        - Provide navigation to the Collections List Screen.
        - Provide quick access to create a new prompt.
        - Provide quick access to create a new collection.
        - Display a loading state while dashboard information is being retrieved.
        - Display an error state if dashboard information cannot be retrieved.
        - Display an appropriate empty state when there is no recent activity.
        - Refresh dashboard information when the user reloads or revisits the screen.

    **API endpoints consumed:**

        - GET    /prompts	Retrieve prompts and determine the total prompt count and recent prompt activity
        - GET	/collections	Retrieve collections and determine the total collection count and recent collection activity

2.  **Prompts List Screen**: 
    *   **Purpose**: Displays a searchable and filterable list of all prompts. Users can filter by collection, filter by tags, and search by title/description. It acts as the primary hub for navigating to individual prompts.

    **Primary functionality:**

        - Display a list of prompts.
        - Display prompt title/name and relevant metadata.
        - Search prompts by text.
        - Filter prompts by collection when supported by the API.
        - Navigate to a prompt's detail/edit view.
        - Provide a way to create a new prompt.
        - Display loading, error, and empty states.

    **API endpoints consumed:**

        - GET /prompts
        - GET /prompts/search if provided by the backend API
        - Collection endpoint(s) required for collection filtering, if applicable.

3.  **Prompt Detail Screen**: 
    *   **Purpose**: Displays the full content of a selected prompt, including its metadata (creation date, associated collection, and tags). Provides actions to edit or delete the prompt.

    **Primary functionality:**

        - Display prompt details.
        - Display the prompt's collection and tags when available.
        - Edit prompt information.
        - Save changes.
        - Delete the prompt.
        - Display validation and API errors.

    **API endpoints consumed:**

        - GET /prompts/{prompt_id}
        - PUT /prompts/{prompt_id} or the update endpoint defined by the backend API.
        - PATCH /prompts/{prompt_id} if supported by the backend.
        - DELETE /prompts/{prompt_id}

4.  **Create/Edit Prompt Screen (Modal/Drawer)**: 
    *   **Purpose**: A form interface allowing users to input a new prompt or update an existing one. Users can specify the title, content, description, assign it to a collection, and attach tags.

    **Primary functionality:**

        - Enter prompt information.
        - Select a collection when applicable.
        - Assign tags when supported.
        - Submit the new prompt.
        - Display validation errors.
        - Return to the prompt list or prompt detail screen after successful creation.

    **API endpoints consumed:**

        - POST /prompts
        - Collection endpoint(s) required to populate the collection selector.
        - Tag endpoint(s) required to populate available tags.

5.  **Collections List Screen**: 
    *   **Purpose**: Displays all available collections, allowing users to create new collections, view existing ones, and delete them.

    **Primary functionality:**

        - Display all available collections.
        - Display collection names and relevant collection information.
        - Provide a Create Collection action.
        - Provide navigation to the Collection Detail Screen for a selected collection.
        - Provide a Delete Collection action.
        - Require confirmation before deleting a collection.
        - Display a loading state while collections are being retrieved.
        - Display an error state if the collection request fails.
        - Display an empty state when no collections exist.
        - Refresh the collection list after a successful create or delete operation.

    **API endpoints consumed:**

        - GET    /collections	Retrieve all collections
        - POST	/collections	Create a new collection
        - DELETE	/collections/{collection_id}	Delete a collection

6.  **Collection Detail Screen**: 
    *   **Purpose**: Displays the details of a specific collection and lists all prompts that belong to it.

    **Primary functionality:**

        - Display the selected collection's details.
        - Display the collection name and other available collection information.
        - Display all prompts associated with the collection.
        - Allow the user to select a prompt to view its details.
        - Provide navigation back to the Collections List Screen.
        - Display a loading state while collection details and associated prompts are being retrieved.
        - Display an error state if the collection or prompt data cannot be retrieved.
        - Display an empty state when the collection contains no prompts.
        - Reflect changes made to the collection or its prompts after successful API operations.

    **API endpoints consumed:**

        - GET   /collections/{collection_id}	Retrieve the details of a specific collection
        - GET	/collections/{collection_id}/prompts	Retrieve prompts belonging to the collection

7.  **Tags Management Screen**: 
    *   **Purpose**: Allows users to create new tags for categorizing prompts and delete tags that are no longer in use.

    **Primary functionality:**

        - Display available tags.
        - Create tags when supported by the backend.
        - Associate tags with prompts when supported.
        - Display loading, error, and empty states.

    **API endpoints consumed:**

        - GET /tags if provided by the backend.
        - POST /tags if provided by the backend.
        - Prompt/tag endpoint(s) defined by the backend API.

## 2. Component Inventory

| Component | Responsibility | Props |
| :--- | :--- | :--- |
| `App` | Defines the main application structure and screen navigation. | None |
| `Navigation` | Provides navigation between major screens. | `currentPath: string` |
| `PromptCard` | Displays a summary of a prompt in a list format. | `prompt: Prompt`, `onEdit: () => void`, `onDelete: () => void` |
| `PromptForm` | Form for creating or updating prompt data. | `initialData?: Prompt`, `collections: Collection[]`, `tags: Tag[]`, `onSubmit: (data: PromptCreate/PromptUpdate) => void` |
| `CollectionCard` | Displays a summary of a collection. | `collection: Collection`, `onClick: () => void`, `onDelete: () => void` |
| `CollectionForm` | Form for creating or updating a collection. | `initialData?: Collection`, `onSubmit: (data: CollectionCreate) => void` |
| `TagList` | Displays tags with options to delete. | `tags: Tag[]`, `onDelete: (tagId: string) => void` |
| `TagForm` | Input form to create a new tag. | `onSubmit: (name: string) => void` |
| `SearchBar` | Input field for searching prompts. | `value: string`, `onChange: (query: string) => void` |
| `FilterDropdown` | Dropdown selector for filtering prompts by collection or tags. | `options: {label: string, value: string}[]`, `selected: string[]`, `onChange: (selected: string[]) => void` |
| `EmptyState` | Displays a message and icon when a list is empty. | `message: string`, `actionLabel?: string`, `onAction?: () => void` |
| `LoadingSpinner` | Displays a visual indicator during API fetches. | `isLoading: boolean` |
| `ConfirmDialog` | Requests confirmation before destructive operations. | `message: string`, `onConfirm: () => void`, `onCancel: () => void` |
| `ErrorToast` | Displays error messages from failed API calls. | `message: string`, `onClose: () => void` |

## 3. API Endpoint Consumption

| Screen | API Endpoints Consumed |
| :--- | :--- |
| **Dashboard Screen** | `GET /prompts`, `GET /collections` (for aggregate counts) |
| **Prompts List Screen** | `GET /prompts` (supports `collection_id`, `search`, `tags` query params) |
| **Prompt Detail Screen** | `GET /prompts/{prompt_id}`, `DELETE /prompts/{prompt_id}` |
| **Create/Edit Prompt Screen** | `POST /prompts`, `PUT /prompts/{prompt_id}`, `GET /collections` (for dropdown), `GET /tags` (for dropdown) |
| **Collections List Screen** | `GET /collections`, `POST /collections`, `DELETE /collections/{collection_id}` |
| **Collection Detail Screen** | `GET /collections/{collection_id}`, `GET /prompts?collection_id={id}` |
| **Tags Management Screen** | `GET /tags`, `POST /tags`, `DELETE /tags/{tag_id}` |

## 4. State Management Approach

*   **Server State (Caching & Fetching)**: Use a data-fetching library like **React Query (TanStack Query)** or **SWR** to handle API requests. This manages caching, background revalidation, and loading/error states for endpoints like `GET /prompts` and `GET /collections`.
*   **Global UI State**: Use **Zustand** or **React Context API** for shared application state that needs to persist across components without prop drilling, such as the currently selected collection filter or the currently active tag filters.
*   **Local Component State**: Use standard React `useState` for isolated UI interactions, such as form inputs, modal open/close toggles, and search bar text before debouncing/submission.

* **API data**: API requests will be handled by a dedicated API/service layer rather than being embedded directly throughout presentation components.

API operations will track:
- Data.
- Loading state.
- Error state.

## 5. Loading, Error, and Empty State Behavior

*   **Loading State**: When an API request is pending (e.g., fetching the list of prompts), display a `LoadingSpinner` component or skeleton placeholders in the specific container to indicate that data is being retrieved.
*   **Error State**: If an API request fails, display an `ErrorToast` or inline error message. For example, if creating a tag with a duplicate name, display the `400 Bad Request` message ("Tag name must be unique"). If deleting a tag that is in use, display the `409 Conflict` message. Where retrying the request is appropriate, the screen will provide a retry action. The frontend will not expose raw stack traces or implementation details to the user. For form submissions, validation or API errors will be displayed near the affected form or as a clear error message.
*   **Empty State**: When an API request succeeds but returns an empty array, display an `EmptyState` component with a relevant message (e.g., No prompts: "No prompts found. Try creating a new prompt!" or No collections: "No collections available." or No search results: "No prompts match your search. Try a different search term."). Empty states will distinguish between:
- No data existing.
- A search/filter producing no results.
- An API request failing.

## 6. Form Behaviour

Create and edit forms will:

- Validate required fields before submitting.
- Prevent submission when required fields are invalid.
- Display validation errors clearly.
- Show a submitting/loading state while the API request is in progress.
- Display an error if the API request fails.
- Update or navigate the UI after a successful request.

Destructive operations such as deletion will require user confirmation before the API request is sent.

## 7. Organizing Principle of Folder Structure

The folder structure is organized by feature/domain to ensure high cohesion and low coupling, grouping all related components, hooks, and API services for a specific feature (e.g., prompts, collections) within the same directory.


Planned structure:

```text
frontend/
├── src/
│   ├── components/
│   │   ├── common/
│   │   ├── prompts/
│   │   ├── collections/
│   │   └── tags/
│   │
│   ├── screens/
│   │   ├── PromptList/
│   │   ├── PromptDetail/
│   │   ├── CreatePrompt/
│   │   ├── Collections/
│   │   └── Tags/
│   │
│   ├── services/
│   │   └── api/
│   │
│   ├── hooks/
│   │
│   ├── types/
│   │
│   ├── App.jsx
│   └── main.jsx
│
├── package.json
└── README.md
```

The exact filenames may change during implementation, but the separation of responsibilities described above will remain the organizing principle of the frontend.
