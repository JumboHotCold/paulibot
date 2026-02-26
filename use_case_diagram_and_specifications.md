# PauliBot — Use Case Diagram & Use Case Specifications

---

## Part 1: Use Case Diagram

### Notation Guide
- **Stick Figure**: Actor (User or External System)
- **Oval/Stadium**: Use Case (Process/Event)
- **Solid Line** (`──`): Association (Direct relationship)
- **Dashed Arrow** (`.->`): Includes `<<include>>` or Extends `<<extend>>`

### System Diagram

```mermaid
graph LR
    subgraph "Primary Users - LEFT"
        Student["🧑 Student / Authenticated"]
        Guest["🧑 Guest User"]
    end

    subgraph "PauliBot System Boundary - CENTER"
        %% The 10 explicit Base & Included/Extended Use Cases %%
        UC1([1. Send Message])
        UC2([2. Send Message - Guest])
        UC3([3. View Chat History])
        UC4([4. Manage Conversations])
        
        UC5([5. Manage Knowledge Base])
        UC6([6. Manage System Users])
        
        UC7([7. Generate AI Response])
        UC8([8. Perform Semantic Search])
        UC9([9. Save Chat History])
        UC10([10. Auto-Generate Embeddings])
    end

    subgraph "Secondary Users - RIGHT"
        Admin["🧑 Admin / Staff"]
        Gemini["🤖 Gemini API"]
    end

    %% === LEFT SIDE ASSOCIATIONS ===
    Student --- UC1
    Student --- UC3
    Student --- UC4
    Guest --- UC2

    %% === RIGHT SIDE ASSOCIATIONS ===
    Admin --- UC5
    Admin --- UC6
    Gemini --- UC7

    %% === INCLUDE & EXTEND RELATIONSHIPS ===
    UC1 -. "<<include>>" .-> UC7
    UC2 -. "<<include>>" .-> UC7
    UC7 -. "<<include>>" .-> UC8
    
    UC1 -. "<<extend>>" .-> UC9
    UC5 -. "<<include>>" .-> UC10
```

---

## Part 2: Use Case Specifications (Exact 1-to-1 Mapping)

---

### UC-01: Send Message

| Field | Details |
|---|---|
| **Use Case Name** | 1. Send Message |
| **Actors** | Student (Primary) |
| **Brief Description** | An authenticated student sends a prompt/question to PauliBot to receive an intelligent answer. |
| **Precondition(s)** | Student is logged into the system and Chat interface is loaded. |
| **Postcondition(s)** | AI response is generated and displayed to the user. |
| **Business Rule** | Empty messages are rejected. |

#### Main Flow / Basic Path

```mermaid
flowchart TD
    A((Start)) --> B[Student types message in chat input]
    B --> C[Student clicks 'Send' button]
    C --> D{Message is empty?}
    D -- No --> E["Include Use Case 7: Generate AI Response"]
    E --> F["Extend Use Case 9: Save Chat History"]
    F --> G[System displays response in chat window]
    G --> H((End))
```

#### Alternative Flow 

```mermaid
flowchart TD
    A((Start)) --> B[Student clicks 'Send' with an empty input box]
    B --> C[System detects empty message]
    C --> D[System displays warning prompt: 'Please type a message.']
    D --> E[Student remains on Chat interface to try again]
    E --> F((End))
```

---

### UC-02: Send Message - Guest

| Field | Details |
|---|---|
| **Use Case Name** | 2. Send Message - Guest |
| **Actors** | Guest User (Primary) |
| **Brief Description** | A guest user submits a question to PauliBot without logging in. Conversations are active but transient. |
| **Precondition(s)** | Guest has accepted terms and is viewing the Chat window. |
| **Postcondition(s)** | Response is displayed. Data is **not** saved. |
| **Business Rule** | Guest sessions are transient (no history preserved). |

#### Main Flow / Basic Path

```mermaid
flowchart TD
    A((Start)) --> B[Guest types question in chat input]
    B --> C[Guest clicks 'Send']
    C --> D{Message is empty?}
    D -- No --> E["Include Use Case 7: Generate AI Response"]
    E --> F[System skips saving logic entirely]
    F --> G[System displays response in chat window]
    G --> H((End))
```

#### Alternative Flow

```mermaid
flowchart TD
    A((Start)) --> B[Guest clicks 'Send' with empty input]
    B --> C[System detects empty message]
    C --> D[System displays warning prompt]
    D --> E[Wait for Guest to try again]
    E --> F((End))
```

---

### UC-03: View Chat History

| Field | Details |
|---|---|
| **Use Case Name** | 3. View Chat History |
| **Actors** | Student (Primary) |
| **Brief Description** | Allows a student to browse and load previous conversations from the sidebar. |
| **Precondition(s)** | Student is logged in. |
| **Postcondition(s)** | Selected conversation messages populate the main chat area. |
| **Business Rule** | Students can only access their own conversation history. |

#### Main Flow / Basic Path

```mermaid
flowchart TD
    A((Start)) --> B[Student opens Chat interface]
    B --> C[System populates sidebar with Conversation titles]
    C --> D[Student clicks a specific Conversation]
    D --> E[System retrieves all ChatHistory linked to that Conversation]
    E --> F[Messages render dynamically in the main chat window]
    F --> G((End))
```

#### Alternative Flow

```mermaid
flowchart TD
    A((Start)) --> B[Student has 0 previous conversations stored]
    B --> C[System loads empty sidebar]
    C --> D[Display 'No past conversations' empty-state graphic]
    D --> E[Prompt student to initiate a new chat]
    E --> F((End))
```

---

### UC-04: Manage Conversations

| Field | Details |
|---|---|
| **Use Case Name** | 4. Manage Conversations |
| **Actors** | Student (Primary) |
| **Brief Description** | A student creates a new conversation thread or deletes an existing thread. |
| **Precondition(s)** | Student is authenticated and viewing the chat. |
| **Postcondition(s)** | Sidebar list is updated; deleted conversations are permanently removed. |
| **Business Rule** | Deleting a conversation triggers a CASCADE delete for all messages inside. |

#### Main Flow / Basic Path

```mermaid
flowchart TD
    A((Start)) --> B{Action Selected?}
    B -- Create New --> C[Student clicks 'New Chat' button]
    C --> D[System allocates empty chat window]
    D --> E((End))

    B -- Delete --> F[Student clicks trash icon on a conversation]
    F --> G[System deletes Conversation and all linked ChatHistory]
    G --> H[Update sidebar list]
    H --> E
```

#### Alternative Flow

```mermaid
flowchart TD
    A((Start)) --> B[Student deletes the conversation that is currently open]
    B --> C[System removes the Conversation from database]
    C --> D[System detects active chat is now null]
    D --> E[System clears the main chat window]
    E --> F[System falls back to 'New Chat' empty-state screen]
    F --> G((End))
```

---

### UC-05: Manage Knowledge Base

| Field | Details |
|---|---|
| **Use Case Name** | 5. Manage Knowledge Base |
| **Actors** | Admin / Staff (Secondary) |
| **Brief Description** | Admin creates, reads, updates, or deletes (CRUD) FAQs, Locations, and Staff records. |
| **Precondition(s)** | Admin logged into Django dashboard with `is_staff=True`. |
| **Postcondition(s)** | Knowledge records updated in the database. |
| **Business Rule** | Modifications to the text must trigger an embedding recalculation. |

#### Main Flow / Basic Path

```mermaid
flowchart TD
    A((Start)) --> B[Admin selects Knowledge Base module]
    B --> C[Admin modifies database entry fields]
    C --> D[Admin clicks 'Save']
    D --> E{Did text content change?}
    E -- Yes --> F["Include Use Case 10: Auto-Generate Embeddings"]
    F --> G[System flashes 'Success' banner]
    G --> H((End))
```

#### Alternative Flow

```mermaid
flowchart TD
    A((Start)) --> B[Admin submits Knowledge Base form]
    B --> C{Validation passed?}
    C -- No --> D[Form submission rejected]
    D --> E[Highlight failing fields in red text]
    E --> F[Admin corrects typos or missing data and resubmits]
    F --> G((End))
    C -- Yes --> H[Proceed to Main Flow]
    H --> G
```

---

### UC-06: Manage System Users

| Field | Details |
|---|---|
| **Use Case Name** | 6. Manage System Users |
| **Actors** | Admin (Secondary) |
| **Brief Description** | Admin controls student accounts by deactivating abusive users or creating manual accounts. |
| **Precondition(s)** | Admin logged in with superuser permissions (`is_superuser=True`). |
| **Postcondition(s)** | Target student account is updated/restricted. |
| **Business Rule** | Admins cannot view plaintext passwords. |

#### Main Flow / Basic Path

```mermaid
flowchart TD
    A((Start)) --> B[Admin navigates to System Users list]
    B --> C[Admin selects a student profile]
    C --> D[Admin unticks the 'is_active' checkbox]
    D --> E[Admin saves the profile]
    E --> F[Student is immediately barred from logging in]
    F --> G((End))
```

#### Alternative Flow

```mermaid
flowchart TD
    A((Start)) --> B[Admin clicks 'Add New User' manually]
    B --> C[Admin inputs Student ID, name, and raw password]
    C --> D[System intercepts save operation]
    D --> E[System hashes password using Django PBKDF2 algorithm]
    E --> F[System safely saves record to database]
    F --> G((End))
```

---

### UC-07: Generate AI Response

| Field | Details |
|---|---|
| **Use Case Name** | 7. Generate AI Response |
| **Actors** | Gemini API (Secondary) |
| **Brief Description** | (Sub-Process). Constructs an strict AI prompt using verified context and fetches the generation from Google Gemini. |
| **Precondition(s)** | Triggered by *Send Message* or *Send Message - Guest*. |
| **Postcondition(s)** | Yields a formulated string response. |
| **Business Rule** | API calls must be wrapped in error-handling logic (try/catch). |

#### Main Flow / Basic Path

```mermaid
flowchart TD
    A((Start)) --> B["Include Use Case 8: Perform Semantic Search"]
    B --> C[System receives filtered text context]
    C --> D[System writes prompt combining Context + Question]
    D --> E[System transmits prompt securely to Gemini API]
    E --> F[Gemini API yields a text string]
    F --> G[System routes string back to chat interface]
    G --> H((End))
```

#### Alternative Flow

```mermaid
flowchart TD
    A((Start)) --> B[System transmits prompt to Gemini API]
    B --> C{Gemini API Reachable?}
    C -- No --> D[API times out or returns error status]
    D --> E[System catches Exception error]
    E --> F[System formulates mechanical apology string]
    F --> G[System routes apology back to chat interface]
    G --> H((End))
```

---

### UC-08: Perform Semantic Search

| Field | Details |
|---|---|
| **Use Case Name** | 8. Perform Semantic Search |
| **Actors** | System (Implicit Backend) |
| **Brief Description** | (Sub-Process). Vectorizes the query and compares it against the Knowledge Base using pgvector distance. |
| **Precondition(s)** | Triggered by *Generate AI Response*. |
| **Postcondition(s)** | Returns top 3 most relevant textual DB entries. |
| **Business Rule** | Relies on the `all-MiniLM-L6-v2` embedding logic. |

#### Main Flow / Basic Path

```mermaid
flowchart TD
    A((Start)) --> B[System parses user's raw message]
    B --> C[Translate message text into 384-dimensional vector string]
    C --> D[Execute L2Distance query across Postgres DB]
    D --> E[Sort matches by geometric closeness]
    E --> F[Slice the top 3 best matching objects]
    F --> G[Format objects into a single readable paragraph]
    G --> H((End))
```

#### Alternative Flow

```mermaid
flowchart TD
    A((Start)) --> B[System compares vectors across Postgres DB]
    B --> C{Are there any matches within acceptable distance?}
    C -- No --> D[Results pool is entirely empty]
    D --> E[System yields an empty context variable]
    E --> F[AI acts entirely blindly with no reference materials]
    F --> G((End))
```

---

### UC-09: Save Chat History

| Field | Details |
|---|---|
| **Use Case Name** | 9. Save Chat History |
| **Actors** | System (Implicit Backend) |
| **Brief Description** | (Sub-Process). Persists chat logs so they can be reviewed by the student later. |
| **Precondition(s)** | Triggered selectively by *Send Message (Authenticated)* via `<<extend>>`. |
| **Postcondition(s)** | ChatHistory tables are updated. |
| **Business Rule** | Messages can only be saved if a linked Conversation thread exists. |

#### Main Flow / Basic Path

```mermaid
flowchart TD
    A((Start)) --> B[System holds the User Query + AI Response]
    B --> C{Does active Conversation ID exist?}
    C -- Yes --> D[Query database for Conversation object]
    D --> E[Write new ChatHistory row linked to Conversation]
    E --> F[Touch Conversation 'updated_at' timestamp parameter]
    F --> G((End))
```

#### Alternative Flow

```mermaid
flowchart TD
    A((Start)) --> B[System checks active Conversation ID]
    B --> C{Conversation ID exists?}
    C -- No --> D[Student just started a brand-new chat session]
    D --> E[System auto-generates a new Conversation object]
    E --> F[System sets object title to the first 30 chars of the message]
    F --> G[Pass new Conversation ID into Main Flow saving logic]
    G --> H((End))
```

---

### UC-10: Auto-Generate Embeddings

| Field | Details |
|---|---|
| **Use Case Name** | 10. Auto-Generate Embeddings |
| **Actors** | System (Implicit Backend) |
| **Brief Description** | (Sub-Process). Generates the AI mathematical vectors whenever Admin modifies knowledge resources. |
| **Precondition(s)** | Triggered heavily by *Manage Knowledge Base* saving. |
| **Postcondition(s)** | PGVector fields populated successfully. |
| **Business Rule** | To save computer power, generation is lazy (calculated only when searched/saved with diffs). |

#### Main Flow / Basic Path

```mermaid
flowchart TD
    A((Start)) --> B[Admin executes a Save event on Knowledge Base]
    B --> C[System deliberately blanks out the old 384-dimension vector field]
    C --> D[Next student search triggers database verify]
    D --> E[System detects a blank field]
    E --> F[Server halts temporarily to run 'all-MiniLM-L6-v2' model over new text]
    F --> G[System writes fresh vector strings into database and resumes]
    G --> H((End))
```

#### Alternative Flow

```mermaid
flowchart TD
    A((Start)) --> B[Admin executes a Save event on Knowledge Base]
    B --> C[System compares old text to newly submitted text]
    C --> D{Is the text strictly identical?}
    D -- Yes --> E[Admin only clicked Save without actually editing]
    E --> F[System skips blanking the vector field to conserve server power]
    F --> G((End))
```
