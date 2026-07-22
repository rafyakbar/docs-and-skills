# Laravel AI SDK

- [Introduction](#introduction)
- [Installation](#installation)
  * [Configuration](#configuration)
  * [Custom Base URLs](#custom-base-urls)
  * [OpenAI-Compatible Providers](#openai-compatible-providers)
  * [Provider Support](#provider-support)
- [Agents](#agents)
  * [Prompting](#prompting)
  * [Conversation Context](#conversation-context)
  * [Structured Output](#structured-output)
  * [Attachments](#attachments)
  * [Streaming](#streaming)
  * [Broadcasting](#broadcasting)
  * [Queueing](#queueing)
  * [Tools](#tools)
  * [File Storage Tools](#file-storage-tools)
  * [MCP Tools](#mcp-tools)
  * [Provider Tools](#provider-tools)
  * [Sub-Agents](#sub-agents)
  * [Middleware](#middleware)
  * [Anonymous Agents](#anonymous-agents)
  * [Agent Configuration](#agent-configuration)
  * [Provider Options](#provider-options)
- [Human Tool Approval](#human-tool-approval)
  * [Complete Approval Flow](#complete-approval-flow)
- [Images](#images)
- [Audio (TTS)](#audio)
- [Transcription (STT)](#transcription)
- [Text Summarization](#text-summarization)
- [Embeddings](#embeddings)
  * [Multimodal Embeddings](#multimodal-embeddings)
  * [Querying Embeddings](#querying-embeddings)
  * [Caching Embeddings](#caching-embeddings)
- [Reranking](#reranking)
- [Files](#files)
- [Vector Stores](#vector-stores)
  * [Adding Files to Stores](#adding-files-to-stores)
- [Failover](#failover)
- [Testing](#testing)
  * [Agents](#testing-agents)
  * [Images](#testing-images)
  * [Audio](#testing-audio)
  * [Transcriptions](#testing-transcriptions)
  * [Embeddings](#testing-embeddings)
  * [Reranking](#testing-reranking)
  * [Files](#testing-files)
  * [Vector Stores](#testing-vector-stores)
- [Events](#events)

## [Introduction](#introduction)

The [Laravel AI SDK](https://github.com/laravel/ai) provides a unified, expressive API for interacting with AI providers such as OpenAI, Anthropic, Gemini, and more. With the AI SDK, you can build intelligent agents with tools and structured output, generate images, synthesize and transcribe audio, create vector embeddings, and much more — all using a consistent, Laravel-friendly interface.

## [Installation](#installation)

You can install the Laravel AI SDK via Composer:

```
1composer require laravel/ai
```

Next, you should publish the AI SDK configuration and migration files using the `vendor:publish` Artisan command:

```
1php artisan vendor:publish --provider="Laravel\Ai\AiServiceProvider"
```

Finally, you should run your application's database migrations. This will create a `agent_conversations` and `agent_conversation_messages` table that the AI SDK uses to power its conversation storage:

```
1php artisan migrate
```

### [Configuration](#configuration)

You may define your AI provider credentials in your application's `config/ai.php` configuration file or as environment variables in your application's `.env` file:

```
 1ANTHROPIC_API_KEY=

 2AZURE_OPENAI_API_KEY=

 3COHERE_API_KEY=

 4DEEPSEEK_API_KEY=

 5ELEVENLABS_API_KEY=

 6GEMINI_API_KEY=

 7GROQ_API_KEY=

 8MISTRAL_API_KEY=

 9OLLAMA_API_KEY=

10OPENAI_API_KEY=

11OPENAI_COMPATIBLE_API_KEY=

12OPENAI_COMPATIBLE_URL=

13OPENROUTER_API_KEY=

14JINA_API_KEY=

15VOYAGEAI_API_KEY=

16XAI_API_KEY=
```

The default models used for text, images, audio, transcription, and embeddings may also be configured in your application's `config/ai.php` configuration file.

### [Custom Base URLs](#custom-base-urls)

By default, the Laravel AI SDK connects directly to each provider's public API endpoint. However, you may need to route requests through a different endpoint - for example, when using a proxy service to centralize API key management, implement rate limiting, or route traffic through a corporate gateway.

You may configure custom base URLs by adding a `url` parameter to your provider configuration:

```
 1'providers' => [

 2    'openai' => [

 3        'driver' => 'openai',

 4        'key' => env('OPENAI_API_KEY'),

 5        'url' => env('OPENAI_URL'),

 6    ],

 7 

 8    'anthropic' => [

 9        'driver' => 'anthropic',

10        'key' => env('ANTHROPIC_API_KEY'),

11        'url' => env('ANTHROPIC_BASE_URL'),

12    ],

13],
```

This is useful when routing requests through a proxy service (such as LiteLLM or Azure OpenAI Gateway) or using alternative endpoints.

Custom base URLs are supported for the following providers: OpenAI, Anthropic, Gemini, Groq, Cohere, DeepSeek, xAI, and OpenRouter.

### [OpenAI-Compatible Providers](#openai-compatible-providers)

If you are using an OpenAI-compatible API, such as LM Studio, vLLM, Together, Fireworks, or a local gateway, you may configure an `openai-compatible` provider. The `url` option is required, while the `key` option is optional and will be sent as a bearer token when present:

```
1'providers' => [

2    'local' => [

3        'driver' => 'openai-compatible',

4        'url' => env('LOCAL_AI_URL'),

5        'key' => env('LOCAL_AI_API_KEY'),

6    ],

7],
```

Once configured, you may use the named provider like any other provider:

```
1agent()->prompt('What is Laravel?', provider: 'local', model: 'local-model');
```

You may also configure a default text model for the provider so that you do not need to pass a model explicitly:

```
 1'local' => [

 2    'driver' => 'openai-compatible',

 3    'url' => env('LOCAL_AI_URL'),

 4    'key' => env('LOCAL_AI_API_KEY'),

 5    'models' => [

 6        'text' => [

 7            'default' => env('LOCAL_AI_MODEL'),

 8        ],

 9    ],

10],
```

OpenAI-compatible providers support text generation, streaming, tools, structured output, and image attachments. If your endpoint requires additional request body fields, provide them using [provider options](#provider-options).

### [Provider Support](#provider-support)

The AI SDK supports a variety of providers across its features. The following table summarizes which providers are available for each feature:

| Feature    | Providers                                                                                                      |
| ---------- | -------------------------------------------------------------------------------------------------------------- |
| Text       | OpenAI, OpenAI Compatible, Anthropic, Gemini, Azure, Bedrock, Groq, xAI, DeepSeek, Mistral, Ollama, OpenRouter |
| Images     | OpenAI, Gemini, xAI, Azure, Bedrock, OpenRouter                                                                |
| TTS        | OpenAI, ElevenLabs, Gemini                                                                                     |
| STT        | OpenAI, ElevenLabs, Mistral, Gemini                                                                            |
| Embeddings | OpenAI, Gemini, Azure, Bedrock, Cohere, Mistral, Jina, VoyageAI, Ollama, OpenRouter                            |
| Reranking  | Cohere, Jina, VoyageAI                                                                                         |
| Files      | OpenAI, Anthropic, Gemini, Azure                                                                               |

The `Laravel\Ai\Enums\Lab` enum may be used to reference providers throughout your code instead of using plain strings:

```
1use Laravel\Ai\Enums\Lab;

2 

3Lab::Anthropic;

4Lab::OpenAI;

5Lab::OpenAiCompatible;

6Lab::Gemini;

7// ...
```

## [Agents](#agents)

Agents are the fundamental building block for interacting with AI providers in the Laravel AI SDK. Each agent is a dedicated PHP class that encapsulates the instructions, conversation context, tools, and output schema needed to interact with a large language model. Think of an agent as a specialized assistant — a sales coach, a document analyzer, a support bot — that you configure once and prompt as needed throughout your application.

You can create an agent via the `make:agent` Artisan command:

```
1php artisan make:agent SalesCoach

2 

3php artisan make:agent SalesCoach --structured
```

Within the generated agent class, you can define the system prompt / instructions, message context, available tools, and output schema (if applicable):

```
 1<?php

 2 

 3namespace App\Ai\Agents;

 4 

 5use App\Ai\Tools\RetrievePreviousTranscripts;

 6use App\Models\History;

 7use App\Models\User;

 8use Illuminate\Contracts\JsonSchema\JsonSchema;

 9use Laravel\Ai\Contracts\Agent;

10use Laravel\Ai\Contracts\Conversational;

11use Laravel\Ai\Contracts\HasStructuredOutput;

12use Laravel\Ai\Contracts\HasTools;

13use Laravel\Ai\Messages\Message;

14use Laravel\Ai\Promptable;

15use Stringable;

16 

17class SalesCoach implements Agent, Conversational, HasTools, HasStructuredOutput

18{

19    use Promptable;

20 

21    public function __construct(public User $user) {}

22 

23    /**

24     * Get the instructions that the agent should follow.

25     */

26    public function instructions(): Stringable|string

27    {

28        return 'You are a sales coach, analyzing transcripts and providing feedback and an overall sales strength score.';

29    }

30 

31    /**

32     * Get the list of messages comprising the conversation so far.

33     */

34    public function messages(): iterable

35    {

36        return History::where('user_id', $this->user->id)

37            ->latest()

38            ->limit(50)

39            ->get()

40            ->reverse()

41            ->map(function ($message) {

42                return new Message($message->role, $message->content);

43            })->all();

44    }

45 

46    /**

47     * Get the tools available to the agent.

48     *

49     * @return Tool[]

50     */

51    public function tools(): iterable

52    {

53        return [

54            new RetrievePreviousTranscripts,

55        ];

56    }

57 

58    /**

59     * Get the agent's structured output schema definition.

60     */

61    public function schema(JsonSchema $schema): array

62    {

63        return [

64            'feedback' => $schema->string()->required(),

65            'score' => $schema->integer()->min(1)->max(10)->required(),

66        ];

67    }

68}
```

### [Prompting](#prompting)

To prompt an agent, first create an instance using the `make` method or standard instantiation, then call `prompt`:

```
1$response = (new SalesCoach)

2    ->prompt('Analyze this sales transcript...');

3 

4return (string) $response;
```

The `make` method resolves your agent from the container, allowing automatic dependency injection. You may also pass arguments to the agent's constructor:

```
1$agent = SalesCoach::make(user: $user);
```

By passing additional arguments to the `prompt` method, you may override the default provider, model, or HTTP timeout when prompting:

```
1$response = (new SalesCoach)->prompt(

2    'Analyze this sales transcript...',

3    provider: Lab::Anthropic,

4    model: 'claude-sonnet-5',

5    timeout: 120,

6);
```

### [Conversation Context](#conversation-context)

If your agent implements the `Conversational` interface, you may use the `messages` method to return the previous conversation context, if applicable:

```
 1use App\Models\History;

 2use Laravel\Ai\Messages\Message;

 3 

 4/**

 5 * Get the list of messages comprising the conversation so far.

 6 */

 7public function messages(): iterable

 8{

 9    return History::where('user_id', $this->user->id)

10        ->latest()

11        ->limit(50)

12        ->get()

13        ->reverse()

14        ->map(function ($message) {

15            return new Message($message->role, $message->content);

16        })->all();

17}
```

#### [Remembering Conversations](#remembering-conversations)

Before using the `RemembersConversations` trait, you should publish and run the AI SDK migrations using the `vendor:publish` Artisan command. These migrations will create the necessary database tables to store conversations.

If you would like Laravel to automatically store and retrieve conversation history for your agent, you may use the `RemembersConversations` trait. This trait provides a simple way to persist conversation messages to the database without manually implementing the `Conversational` interface:

```
 1<?php

 2 

 3namespace App\Ai\Agents;

 4 

 5use Laravel\Ai\Concerns\RemembersConversations;

 6use Laravel\Ai\Contracts\Agent;

 7use Laravel\Ai\Contracts\Conversational;

 8use Laravel\Ai\Promptable;

 9 

10class SalesCoach implements Agent, Conversational

11{

12    use Promptable, RemembersConversations;

13 

14    /**

15     * Get the instructions that the agent should follow.

16     */

17    public function instructions(): string

18    {

19        return 'You are a sales coach...';

20    }

21}
```

When using the `RemembersConversations` trait, do not manually define a `messages` method in your agent class. If a `messages` method is present, it will take precedence over the trait's implementation and conversation history will not be loaded from the database.

To start a new conversation for a user, call the `forUser` method before prompting:

```
1$response = (new SalesCoach)->forUser($user)->prompt('Hello!');

2 

3$conversationId = $response->conversationId;
```

The conversation ID is returned on the response and can be stored for future reference. If you would like to retrieve all of a user's conversations using Eloquent, you may add the `HasConversations` trait to your user model:

```
 1<?php

 2 

 3namespace App\Models;

 4 

 5use Illuminate\Foundation\Auth\User as Authenticatable;

 6use Laravel\Ai\Concerns\HasConversations;

 7 

 8class User extends Authenticatable

 9{

10    use HasConversations;

11}
```

Once the trait has been added to your model, you may retrieve and query the user's conversations via the `conversations` relationship:

```
1$conversations = $user->conversations()

2    ->latest('updated_at')

3    ->paginate(20);
```

To continue an existing conversation, use the `continue` method:

```
1$response = (new SalesCoach)

2    ->continue($conversationId, as: $user)

3    ->prompt('Tell me more about that.');
```

When using the `RemembersConversations` trait, previous messages are automatically loaded and included in the conversation context when prompting. New messages (both user and assistant) are automatically stored after each interaction.

#### [Conversation Participants](#conversation-participants)

Although users are the most common conversation participants, conversations may belong to any Eloquent model. Use the `forParticipant` method to start a conversation for another type of model:

```
1$response = (new SalesCoach)

2    ->forParticipant($team)

3    ->prompt('Review our latest sales results.');
```

The participant's morph class and primary key are stored with the conversation. Therefore, models of different types that have the same primary key, such as `User` ID `1` and `Team` ID `1`, have separate conversation histories. The `forUser` method is an alias for `forParticipant`.

You may continue the participant's most recent conversation using the `continueLastConversation` method:

```
1$response = (new SalesCoach)

2    ->continueLastConversation($team)

3    ->prompt('Tell me more about that.');
```

When continuing a specific conversation, pass the participant to the `continue` method:

```
1$response = (new SalesCoach)

2    ->continue($conversationId, as: $team)

3    ->prompt('Tell me more about that.');
```

The `HasConversations` trait may be added to any Eloquent model that participates in conversations. The resulting `conversations` relationship is a polymorphic relationship scoped to that model's type and primary key. You may also access the participant that owns a conversation through its inverse relationship:

```
1$conversations = $team->conversations;

2 

3$participant = $conversation->participant;
```

If your application uses multiple participant model types, you should consider defining an [Eloquent morph map](/docs/13.x/eloquent-relationships#custom-polymorphic-types) so that stored participant types are not coupled to your model class names.

The `continue` method does not verify that the given participant owns the conversation. Your application should authorize access to the conversation before continuing it.

### [Structured Output](#structured-output)

If you would like your agent to return structured output, implement the `HasStructuredOutput` interface, which requires that your agent define a `schema` method:

```
 1<?php

 2 

 3namespace App\Ai\Agents;

 4 

 5use Illuminate\Contracts\JsonSchema\JsonSchema;

 6use Laravel\Ai\Contracts\Agent;

 7use Laravel\Ai\Contracts\HasStructuredOutput;

 8use Laravel\Ai\Promptable;

 9 

10class SalesCoach implements Agent, HasStructuredOutput

11{

12    use Promptable;

13 

14    // ...

15 

16    /**

17     * Get the agent's structured output schema definition.

18     */

19    public function schema(JsonSchema $schema): array

20    {

21        return [

22            'score' => $schema->integer()->required(),

23        ];

24    }

25}
```

When prompting an agent that returns structured output, you can access the returned `StructuredAgentResponse` like an array:

```
1$response = (new SalesCoach)->prompt('Analyze this sales transcript...');

2 

3return $response['score'];
```

#### [Nested Objects](#structured-output-nested-objects)

To define nested structured output, use the `object` method with a closure:

```
 1<?php

 2 

 3namespace App\Ai\Agents;

 4 

 5use Illuminate\Contracts\JsonSchema\JsonSchema;

 6use Laravel\Ai\Contracts\Agent;

 7use Laravel\Ai\Contracts\HasStructuredOutput;

 8use Laravel\Ai\Promptable;

 9 

10class SalesCoach implements Agent, HasStructuredOutput

11{

12    use Promptable;

13 

14    // ...

15 

16    /**

17     * Get the agent's structured output schema definition.

18     */

19    public function schema(JsonSchema $schema): array

20    {

21        return [

22            'score' => $schema->integer()->required(),

23            'metadata' => $schema->object(fn ($schema) => [

24                'confidence' => $schema->string()->enum(['low', 'medium', 'high'])->required(),

25                'language' => $schema->string()->required(),

26            ])->required(),

27        ];

28    }

29}
```

#### [Arrays of Objects](#structured-output-arrays-of-objects)

If your agent should return a list of structured items, combine the `array` and `object` methods:

```
 1public function schema(JsonSchema $schema): array

 2{

 3    return [

 4        'feedback' => $schema->array()

 5            ->items(

 6                $schema->object(fn ($schema) => [

 7                    'comment' => $schema->string()->required(),

 8                    'score' => $schema->integer()->required(),

 9                ])

10            )

11            ->required(),

12    ];

13}
```

If a value may match one of several schemas, use the `anyOf` method:

```
 1public function schema(JsonSchema $schema): array

 2{

 3    return [

 4        'content' => $schema->anyOf([

 5            $schema->object(fn ($schema) => [

 6                'type' => $schema->string()->enum(['article'])->required(),

 7                'title' => $schema->string()->required(),

 8            ]),

 9            $schema->object(fn ($schema) => [

10                'type' => $schema->string()->enum(['image'])->required(),

11                'url' => $schema->string()->required(),

12            ]),

13        ])->required(),

14    ];

15}
```

### [Attachments](#attachments)

When prompting, you may also pass attachments with the prompt to allow the model to inspect images and documents:

```
 1use App\Ai\Agents\SalesCoach;

 2use Laravel\Ai\Files;

 3 

 4$response = (new SalesCoach)->prompt(

 5    'Analyze the attached sales transcript...',

 6    attachments: [

 7        Files\Document::fromStorage('transcript.pdf') // Attach a document from a filesystem disk...

 8        Files\Document::fromPath('/home/laravel/transcript.md') // Attach a document from a local path...

 9        $request->file('transcript'), // Attach an uploaded file...

10    ]

11);
```

Likewise, the `Laravel\Ai\Files\Image` class may be used to attach images to a prompt:

```
 1use App\Ai\Agents\ImageAnalyzer;

 2use Laravel\Ai\Files;

 3 

 4$response = (new ImageAnalyzer)->prompt(

 5    'What is in this image?',

 6    attachments: [

 7        Files\Image::fromStorage('photo.jpg') // Attach an image from a filesystem disk...

 8        Files\Image::fromPath('/home/laravel/photo.jpg') // Attach an image from a local path...

 9        $request->file('photo'), // Attach an uploaded file...

10    ]

11);
```

### [Streaming](#streaming)

You may stream an agent's response by invoking the `stream` method. The returned `StreamableAgentResponse` may be returned from a route to automatically send a streaming response (SSE) to the client:

```
1use App\Ai\Agents\SalesCoach;

2 

3Route::get('/coach', function () {

4    return (new SalesCoach)->stream('Analyze this sales transcript...');

5});
```

The `then` method may be used to provide a closure that will be invoked when the entire response has been streamed to the client:

```
 1use App\Ai\Agents\SalesCoach;

 2use Laravel\Ai\Responses\StreamedAgentResponse;

 3 

 4Route::get('/coach', function () {

 5    return (new SalesCoach)

 6        ->stream('Analyze this sales transcript...')

 7        ->then(function (StreamedAgentResponse $response) {

 8            // $response->text, $response->events, $response->usage...

 9        });

10});
```

Alternatively, you may iterate through the streamed events manually:

```
1$stream = (new SalesCoach)->stream('Analyze this sales transcript...');

2 

3foreach ($stream as $event) {

4    // ...

5}
```

#### [Streaming Using the Vercel AI SDK Protocol](#streaming-using-the-vercel-ai-sdk-protocol)

You may stream the events using the [Vercel AI SDK stream protocol](https://ai-sdk.dev/docs/ai-sdk-ui/stream-protocol) by invoking the `usingVercelDataProtocol` method on the streamable response:

```
1use App\Ai\Agents\SalesCoach;

2 

3Route::get('/coach', function () {

4    return (new SalesCoach)

5        ->stream('Analyze this sales transcript...')

6        ->usingVercelDataProtocol();

7});
```

### [Broadcasting](#broadcasting)

You may broadcast streamed events in a few different ways. First, you can simply invoke the `broadcast` or `broadcastNow` method on a streamed event:

```
1use App\Ai\Agents\SalesCoach;

2use Illuminate\Broadcasting\Channel;

3 

4$stream = (new SalesCoach)->stream('Analyze this sales transcript...');

5 

6foreach ($stream as $event) {

7    $event->broadcast(new Channel('channel-name'));

8}
```

Or, you can invoke an agent's `broadcastOnQueue` method to queue the agent operation and broadcast the streamed events as they are available:

```
1(new SalesCoach)->broadcastOnQueue(

2    'Analyze this sales transcript...'

3    new Channel('channel-name'),

4);
```

#### [Skipping Oversized Events](#skipping-oversized-events)

Some broadcasting platforms limit WebSocket messages to around 10KB. Data-heavy stream events, like large tool results, can exceed this limit and cause broadcasting to fail. You may exclude specific event types from broadcasting using the `WithoutBroadcasting` attribute:

```
 1<?php

 2 

 3namespace App\Ai\Agents;

 4 

 5use Laravel\Ai\Attributes\WithoutBroadcasting;

 6use Laravel\Ai\Contracts\Agent;

 7use Laravel\Ai\Contracts\HasTools;

 8use Laravel\Ai\Promptable;

 9use Laravel\Ai\Streaming\Events\ToolCall;

10use Laravel\Ai\Streaming\Events\ToolResult;

11 

12#[WithoutBroadcasting(ToolCall::class, ToolResult::class)]

13class SearchAgent implements Agent, HasTools

14{

15    use Promptable;

16 

17    // ...

18}
```

The excluded events are never broadcast, but they are still persisted to the `agent_conversation_messages` table, so your frontend can load the full tool data after the stream completes. This works for both queued (`broadcastOnQueue`) and synchronous (`broadcast` / `broadcastNow`) broadcasting.

### [Queueing](#queueing)

Using an agent's `queue` method, you may prompt the agent, but allow it to process the response in the background, keeping your application feeling fast and responsive. The `then` and `catch` methods may be used to register closures that will be invoked when a response is available or if an exception occurs:

```
 1use Illuminate\Http\Request;

 2use Laravel\Ai\Responses\AgentResponse;

 3use Throwable;

 4 

 5Route::post('/coach', function (Request $request) {

 6    (new SalesCoach)

 7        ->queue($request->input('transcript'))

 8        ->then(function (AgentResponse $response) {

 9            // ...

10        })

11        ->catch(function (Throwable $e) {

12            // ...

13        });

14 

15    return back();

16});
```

### [Tools](#tools)

Tools may be used to give agents additional functionality that they can utilize while responding to prompts. Tools can be created using the `make:tool` Artisan command:

```
1php artisan make:tool RandomNumberGenerator
```

The generated tool will be placed in your application's `app/Ai/Tools` directory. Each tool contains a `handle` method that will be invoked by the agent when it needs to utilize the tool:

```
 1<?php

 2 

 3namespace App\Ai\Tools;

 4 

 5use Illuminate\Contracts\JsonSchema\JsonSchema;

 6use Laravel\Ai\Contracts\Tool;

 7use Laravel\Ai\Tools\Request;

 8use Stringable;

 9 

10class RandomNumberGenerator implements Tool

11{

12    /**

13     * Get the description of the tool's purpose.

14     */

15    public function description(): Stringable|string

16    {

17        return 'This tool may be used to generate cryptographically secure random numbers.';

18    }

19 

20    /**

21     * Execute the tool.

22     */

23    public function handle(Request $request): Stringable|string

24    {

25        return (string) random_int($request['min'], $request['max']);

26    }

27 

28    /**

29     * Get the tool's schema definition.

30     */

31    public function schema(JsonSchema $schema): array

32    {

33        return [

34            'min' => $schema->integer()->min(0)->required(),

35            'max' => $schema->integer()->required(),

36        ];

37    }

38}
```

Once you have defined your tool, you may return it from the `tools` method of any of your agents:

```
 1use App\Ai\Tools\RandomNumberGenerator;

 2 

 3/**

 4 * Get the tools available to the agent.

 5 *

 6 * @return Tool[]

 7 */

 8public function tools(): iterable

 9{

10    return [

11        new RandomNumberGenerator,

12    ];

13}
```

#### [Similarity Search](#similarity-search)

The `SimilaritySearch` tool allows agents to search for documents similar to a given query using vector embeddings stored in your database. This is useful for retrieval-augmented generation (RAG) when you want to give agents access to search your application's data.

The simplest way to create a similarity search tool is using the `usingModel` method with an Eloquent model that has vector embeddings:

```
1use App\Models\Document;

2use Laravel\Ai\Tools\SimilaritySearch;

3 

4public function tools(): iterable

5{

6    return [

7        SimilaritySearch::usingModel(Document::class, 'embedding'),

8    ];

9}
```

The first argument is the Eloquent model class, and the second argument is the column containing the vector embeddings.

You may also provide a minimum similarity threshold between `0.0` and `1.0` and a closure to customize the query:

```
1SimilaritySearch::usingModel(

2    model: Document::class,

3    column: 'embedding',

4    minSimilarity: 0.7,

5    limit: 10,

6    query: fn ($query) => $query->where('published', true),

7),
```

For more control, you may create a similarity search tool with a custom closure that returns the search results:

```
 1use App\Models\Document;

 2use Laravel\Ai\Tools\SimilaritySearch;

 3 

 4public function tools(): iterable

 5{

 6    return [

 7        new SimilaritySearch(using: function (string $query) {

 8            return Document::query()

 9                ->where('user_id', $this->user->id)

10                ->whereVectorSimilarTo('embedding', $query)

11                ->limit(10)

12                ->get();

13        }),

14    ];

15}
```

You may customize the tool's description using the `withDescription` method:

```
1SimilaritySearch::usingModel(Document::class, 'embedding')

2    ->withDescription('Search the knowledge base for relevant articles.'),
```

### [File Storage Tools](#file-storage-tools)

The `FileStorage` tool factory allows you to give agents access to a Laravel [filesystem disk](/docs/13.x/filesystem). The `all` method returns tools that allow the agent to list, read, inspect, generate URLs for, write, delete, and copy files on the given disk:

```
1use Laravel\Ai\Tools\FileStorage;

2 

3public function tools(): iterable

4{

5    return FileStorage::all('local');

6}
```

If your agent should only be able to inspect files, use the `readOnly` method:

```
1return FileStorage::readOnly('local');
```

These methods return an `Illuminate\Support\Collection`, allowing you to further filter the tools that are provided to the agent:

```
1use Laravel\Ai\Tools\Filesystem\DeleteFile;

2 

3return FileStorage::all('s3')

4    ->reject(fn ($tool) => $tool instanceof DeleteFile);
```

### [MCP Tools](#mcp-tools)

If your application uses [Laravel MCP](/docs/13.x/mcp), you may give your agents tools exposed by [Model Context Protocol](https://modelcontextprotocol.io) servers. Using the [Laravel MCP client](/docs/13.x/mcp#client), you may connect to a remote or local MCP server and pass its tools directly to your agent.

MCP tools require the [Laravel MCP](/docs/13.x/mcp) package to be installed in your application.

Because an MCP client's `tools` method returns a collection, spread it into your agent's `tools` array using the `...` operator:

```
 1use App\Ai\Tools\RandomNumberGenerator;

 2use Laravel\Mcp\Client;

 3 

 4/**

 5 * Get the tools available to the agent.

 6 *

 7 * @return Tool[]

 8 */

 9public function tools(): iterable

10{

11    return [

12        ...Client::web('https://mcp.example.com')

13            ->withToken($token)

14            ->tools(),

15 

16        new RandomNumberGenerator,

17    ];

18}
```

The AI SDK automatically wraps each MCP tool so the agent can call it like any other tool. You may also use a [named MCP client](/docs/13.x/mcp#named-clients):

```
1use Laravel\Mcp\Facades\Mcp;

2 

3public function tools(): iterable

4{

5    return [

6        ...Mcp::client('github')->tools(),

7    ];

8}
```

Or connect to a [local MCP server](/docs/13.x/mcp#client-connecting):

```
1use Laravel\Mcp\Client;

2 

3public function tools(): iterable

4{

5    return [

6        ...Client::local('php', ['artisan', 'mcp:start'])->tools(),

7    ];

8}
```

For more information on creating and authenticating MCP clients, including bearer tokens and OAuth, consult the [MCP client documentation](/docs/13.x/mcp#client).

### [Provider Tools](#provider-tools)

Provider tools are special tools implemented natively by AI providers, offering capabilities like web searching, URL fetching, and file searching. Unlike regular tools, provider tools are executed by the provider itself rather than your application.

Provider tools can be returned by your agent's `tools` method.

#### [Web Search](#web-search)

The `WebSearch` provider tool allows agents to search the web for real-time information. This is useful for answering questions about current events, recent data, or topics that may have changed since the model's training cutoff.

**Supported providers:** Anthropic, OpenAI, Gemini, OpenRouter

```
1use Laravel\Ai\Providers\Tools\WebSearch;

2 

3public function tools(): iterable

4{

5    return [

6        new WebSearch,

7    ];

8}
```

You may configure the web search tool to limit the number of searches or restrict results to specific domains:

```
1(new WebSearch)->max(5)->allow(['laravel.com', 'php.net']),
```

To refine search results based on user location, use the `location` method:

```
1(new WebSearch)->location(

2    city: 'New York',

3    region: 'NY',

4    country: 'US'

5);
```

#### [Web Fetch](#web-fetch)

The `WebFetch` provider tool allows agents to fetch and read the contents of web pages. This is useful when you need the agent to analyze specific URLs or retrieve detailed information from known web pages.

**Supported providers:** Anthropic, Gemini

```
1use Laravel\Ai\Providers\Tools\WebFetch;

2 

3public function tools(): iterable

4{

5    return [

6        new WebFetch,

7    ];

8}
```

You may configure the web fetch tool to limit the number of fetches or restrict to specific domains:

```
1(new WebFetch)->max(3)->allow(['docs.laravel.com']),
```

#### [File Search](#file-search)

The `FileSearch` provider tool allows agents to search through [files](#files) stored in [vector stores](#vector-stores). This enables retrieval-augmented generation (RAG) by allowing the agent to search your uploaded documents for relevant information.

**Supported providers:** OpenAI, Gemini

```
1use Laravel\Ai\Providers\Tools\FileSearch;

2 

3public function tools(): iterable

4{

5    return [

6        new FileSearch(stores: ['store_id']),

7    ];

8}
```

You may provide multiple vector store IDs to search across multiple stores:

```
1new FileSearch(stores: ['store_1', 'store_2']);
```

If your files have [metadata](#adding-files-to-stores), you may filter the search results by providing a `where` argument. For simple equality filters, pass an array:

```
1new FileSearch(stores: ['store_id'], where: [

2    'author' => 'Taylor Otwell',

3    'year' => 2026,

4]);
```

For more complex filters, you may pass a closure that receives a `FileSearchQuery` instance:

```
1use Laravel\Ai\Providers\Tools\FileSearchQuery;

2 

3new FileSearch(stores: ['store_id'], where: fn (FileSearchQuery $query) =>

4    $query->where('author', 'Taylor Otwell')

5        ->whereNot('status', 'draft')

6        ->whereIn('category', ['news', 'updates'])

7);
```

### [Sub-Agents](#sub-agents)

Agents may also be returned from another agent's `tools` method. When an agent is returned as a tool, the parent agent may delegate a specific task to the sub-agent and use the sub-agent's response while answering the original prompt. This is useful when a general-purpose agent needs access to specialized agents with their own instructions, tools, model configuration, or provider preferences.

For example, a customer support agent could delegate refund eligibility questions to a dedicated refunds agent:

```
 1<?php

 2 

 3namespace App\Ai\Agents;

 4 

 5use Laravel\Ai\Contracts\Agent;

 6use Laravel\Ai\Contracts\HasTools;

 7use Laravel\Ai\Promptable;

 8 

 9class CustomerSupportAgent implements Agent, HasTools

10{

11    use Promptable;

12 

13    /**

14     * Get the instructions that the agent should follow.

15     */

16    public function instructions(): string

17    {

18        return 'You help customers with account, order, and billing questions. Delegate refund policy questions to the refunds specialist.';

19    }

20 

21    /**

22     * Get the tools available to the agent.

23     *

24     * @return Tool[]

25     */

26    public function tools(): iterable

27    {

28        return [

29            new RefundsAgent,

30        ];

31    }

32}
```

To customize how the sub-agent is exposed to the parent agent, implement the `CanActAsTool` interface on the sub-agent and define a tool-facing name and description:

```
 1<?php

 2 

 3namespace App\Ai\Agents;

 4 

 5use App\Ai\Tools\LookupOrder;

 6use Laravel\Ai\Attributes\Provider;

 7use Laravel\Ai\Contracts\Agent;

 8use Laravel\Ai\Contracts\CanActAsTool;

 9use Laravel\Ai\Contracts\HasTools;

10use Laravel\Ai\Enums\Lab;

11use Laravel\Ai\Promptable;

12 

13#[Provider(Lab::Anthropic)]

14class RefundsAgent implements Agent, CanActAsTool, HasTools

15{

16    use Promptable;

17 

18    /**

19     * Get the instructions that the agent should follow.

20     */

21    public function instructions(): string

22    {

23        return 'You are a refunds specialist. Use order details and the refund policy to give concise eligibility guidance.';

24    }

25 

26    /**

27     * Get the agent's tool name.

28     */

29    public function name(): string

30    {

31        return 'refunds_specialist';

32    }

33 

34    /**

35     * Get the agent's tool description.

36     */

37    public function description(): string

38    {

39        return 'Determine whether an order is eligible for a refund and explain the next step.';

40    }

41 

42    /**

43     * Get the tools available to the agent.

44     *

45     * @return Tool[]

46     */

47    public function tools(): iterable

48    {

49        return [

50            new LookupOrder,

51        ];

52    }

53}
```

If a sub-agent does not implement `CanActAsTool`, Laravel will use the agent's class basename as the tool name and a generic description that asks the parent agent to pass a clear, self-contained task description. Each sub-agent invocation runs in isolation and does not receive the parent agent's conversation history.

### [Middleware](#middleware)

Agents support middleware, allowing you to intercept and modify prompts before they are sent to the provider. Middleware can be created using the `make:agent-middleware` Artisan command:

```
1php artisan make:agent-middleware LogPrompts
```

The generated middleware will be placed in your application's `app/Ai/Middleware` directory. To add middleware to an agent, implement the `HasMiddleware` interface and define a `middleware` method that returns an array of middleware classes:

```
 1<?php

 2 

 3namespace App\Ai\Agents;

 4 

 5use App\Ai\Middleware\LogPrompts;

 6use Laravel\Ai\Contracts\Agent;

 7use Laravel\Ai\Contracts\HasMiddleware;

 8use Laravel\Ai\Promptable;

 9 

10class SalesCoach implements Agent, HasMiddleware

11{

12    use Promptable;

13 

14    // ...

15 

16    /**

17     * Get the agent's middleware.

18     */

19    public function middleware(): array

20    {

21        return [

22            new LogPrompts,

23        ];

24    }

25}
```

Each middleware class should define a `handle` method that receives the `AgentPrompt` and a `Closure` to pass the prompt to the next middleware:

```
 1<?php

 2 

 3namespace App\Ai\Middleware;

 4 

 5use Closure;

 6use Laravel\Ai\Prompts\AgentPrompt;

 7 

 8class LogPrompts

 9{

10    /**

11     * Handle the incoming prompt.

12     */

13    public function handle(AgentPrompt $prompt, Closure $next)

14    {

15        Log::info('Prompting agent', ['prompt' => $prompt->prompt]);

16 

17        return $next($prompt);

18    }

19}
```

You may use the `then` method on the response to execute code after the agent has finished processing. This works for both synchronous and streaming responses:

```
1public function handle(AgentPrompt $prompt, Closure $next)

2{

3    return $next($prompt)->then(function (AgentResponse $response) {

4        Log::info('Agent responded', ['text' => $response->text]);

5    });

6}
```

### [Anonymous Agents](#anonymous-agents)

Sometimes you may want to quickly interact with a model without creating a dedicated agent class. You can create an ad-hoc, anonymous agent using the `agent` function:

```
1use function Laravel\Ai\{agent};

2 

3$response = agent(

4    instructions: 'You are an expert at software development.',

5    messages: [],

6    tools: [],

7)->prompt('Tell me about Laravel')
```

Anonymous agents may also produce structured output:

```
1use Illuminate\Contracts\JsonSchema\JsonSchema;

2 

3use function Laravel\Ai\{agent};

4 

5$response = agent(

6    schema: fn (JsonSchema $schema) => [

7        'number' => $schema->integer()->required(),

8    ],

9)->prompt('Generate a random number less than 100')
```

### [Agent Configuration](#agent-configuration)

You may configure text generation options for an agent using PHP attributes. The following attributes are available:

- `MaxSteps`: The maximum number of steps the agent may take when using tools.
- `MaxTokens`: The maximum number of tokens the model may generate.
- `Model`: The model the agent should use.
- `Provider`: The AI provider (or providers for failover) to use for the agent.
- `Temperature`: The sampling temperature to use for generation (0.0 to 1.0).
- `Timeout`: The HTTP timeout in seconds for agent requests (default: 60).
- `TopP`: The nucleus sampling probability to use for generation (0.0 to 1.0).
- `UseCheapestModel`: Use the provider's cheapest text model for cost optimization.
- `UseSmartestModel`: Use the provider's most capable text model for complex tasks.

```
 1<?php

 2 

 3namespace App\Ai\Agents;

 4 

 5use Laravel\Ai\Attributes\MaxSteps;

 6use Laravel\Ai\Attributes\MaxTokens;

 7use Laravel\Ai\Attributes\Model;

 8use Laravel\Ai\Attributes\Provider;

 9use Laravel\Ai\Attributes\Temperature;

10use Laravel\Ai\Attributes\Timeout;

11use Laravel\Ai\Attributes\TopP;

12use Laravel\Ai\Contracts\Agent;

13use Laravel\Ai\Enums\Lab;

14use Laravel\Ai\Promptable;

15 

16#[Provider(Lab::Anthropic)]

17#[Model('claude-sonnet-5')]

18#[MaxSteps(10)]

19#[MaxTokens(4096)]

20#[Temperature(0.7)]

21#[Timeout(120)]

22#[TopP(0.9)]

23class SalesCoach implements Agent

24{

25    use Promptable;

26 

27    // ...

28}
```

The `UseCheapestModel` and `UseSmartestModel` attributes allow you to automatically select the most cost-effective or most capable model for a given provider without specifying a model name. This is useful when you want to optimize for cost or capability across different providers:

```
 1use Laravel\Ai\Attributes\UseCheapestModel;

 2use Laravel\Ai\Attributes\UseSmartestModel;

 3use Laravel\Ai\Contracts\Agent;

 4use Laravel\Ai\Promptable;

 5 

 6#[UseCheapestModel]

 7class SimpleSummarizer implements Agent

 8{

 9    use Promptable;

10 

11    // Will use the cheapest model (e.g., Haiku)...

12}

13 

14#[UseSmartestModel]

15class ComplexReasoner implements Agent

16{

17    use Promptable;

18 

19    // Will use the most capable model (e.g., Opus)...

20}
```

The underlying model selected by `UseCheapestModel` and `UseSmartestModel` may change between releases of the Laravel AI SDK as providers release new models. Switching models can introduce behavioral changes, deprecated parameters, and significant cost differences. If you need a stable, predictable model and pricing, specify the model explicitly using the `Model` attribute.

### [Provider Options](#provider-options)

If your agent needs to pass provider-specific options (such as OpenAI reasoning effort or penalty settings), implement the `HasProviderOptions` contract and define a `providerOptions` method:

```
 1<?php

 2 

 3namespace App\Ai\Agents;

 4 

 5use Laravel\Ai\Contracts\Agent;

 6use Laravel\Ai\Contracts\HasProviderOptions;

 7use Laravel\Ai\Enums\Lab;

 8use Laravel\Ai\Promptable;

 9 

10class SalesCoach implements Agent, HasProviderOptions

11{

12    use Promptable;

13 

14    // ...

15 

16    /**

17     * Get provider-specific generation options.

18     */

19    public function providerOptions(Lab|string $provider): array

20    {

21        return match ($provider) {

22            Lab::OpenAI => [

23                'reasoning' => ['effort' => 'low'],

24                'frequency_penalty' => 0.5,

25                'presence_penalty' => 0.3,

26            ],

27            Lab::Anthropic => [

28                'thinking' => ['budget_tokens' => 1024],

29                'cache_control' => ['type' => 'ephemeral'],

30            ],

31            default => [],

32        };

33    }

34}
```

The `providerOptions` method receives the provider currently being used (`Lab` enum or string), allowing you to return different options per provider. This is especially useful when using [failover](#failover), since each fallback provider can receive its own configuration.

The Anthropic example above also enables [prompt caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching) via `cache_control`.

## [Human Tool Approval](#human-tool-approval)

Tool approval requires a `Conversational` agent whose conversation history is persisted so the paused call can be resumed. The `RemembersConversations` trait provides the necessary persistence.

Tools that perform sensitive or irreversible actions may require human approval before they are executed. To make a tool approvable, implement the `Approvable` contract and use the `InteractsWithApprovals` trait. Approvable tools require approval by default:

```
 1<?php

 2 

 3namespace App\Ai\Tools;

 4 

 5use Illuminate\Contracts\JsonSchema\JsonSchema;

 6use Illuminate\Support\Facades\Storage;

 7use Laravel\Ai\Concerns\InteractsWithApprovals;

 8use Laravel\Ai\Contracts\Approvable;

 9use Laravel\Ai\Contracts\Tool;

10use Laravel\Ai\Tools\Request;

11use Stringable;

12 

13class DeleteFile implements Approvable, Tool

14{

15    use InteractsWithApprovals;

16 

17    /**

18     * Get the description of the tool's purpose.

19     */

20    public function description(): Stringable|string

21    {

22        return 'Delete a file from storage.';

23    }

24 

25    /**

26     * Execute the tool.

27     */

28    public function handle(Request $request): Stringable|string

29    {

30        Storage::delete($request['path']);

31 

32        return "Deleted [{$request['path']}].";

33    }

34 

35    /**

36     * Get the tool's schema definition.

37     */

38    public function schema(JsonSchema $schema): array

39    {

40        return [

41            'path' => $schema->string()->required(),

42        ];

43    }

44}
```

To determine whether approval is needed based on the tool call's arguments, define a `needsApproval` method on the tool. This method may return a boolean or an `Approval` instance that includes a reason for the approval request:

```
 1use Laravel\Ai\Approvals\Approval;

 2 

 3/**

 4 * Determine whether the tool needs approval for the given request.

 5 */

 6protected function needsApproval(Request $request): Approval|bool

 7{

 8    return str_starts_with($request['path'], 'temporary/')

 9        ? false

10        : Approval::required('This will permanently delete a file.');

11}
```

You may override a tool's approval requirement when returning it from an agent's `tools` method:

```
1public function tools(): iterable

2{

3    return [

4        (new SendNotification)->withoutApproval(),

5        (new DeleteFile)->requireApproval('Deletion review required.'),

6    ];

7}
```

When an approvable tool is called, the agent pauses before executing it. You may inspect the response's pending approvals, which contain each tool call's ID, tool name, arguments, and approval reason:

```
 1$response = (new FileAssistant)

 2    ->forUser($user)

 3    ->prompt('Delete the old invoice.');

 4 

 5if ($response->hasPendingApprovals()) {

 6    foreach ($response->pendingApprovals as $approval) {

 7        // $approval->id

 8        // $approval->tool

 9        // $approval->arguments

10        // $approval->reason

11    }

12}
```

To resume the agent, continue the conversation and provide a `Decisions` instance containing a decision for each pending tool call. Decisions may approve the call, reject it, or edit its arguments before execution:

```
1use Laravel\Ai\Approvals\Decision;

2use Laravel\Ai\Approvals\Decisions;

3 

4$response = (new FileAssistant)

5    ->continue($conversationId, as: $user)

6    ->prompt(Decisions::from([

7        'call_abc' => Decision::approve(),

8        'call_ghi' => Decision::reject('The invoice must be retained.'),

9    ]));
```

The boolean values `true` and `false` may be used as shorthand for approval and rejection. Every pending tool call must receive a decision. Unknown, missing, or previously resolved tool call IDs will cause an `ApprovalMismatchException` to be thrown. You may provide a default for calls without an explicit decision using the `approveRemaining` or `rejectRemaining` methods:

```
1$decisions = Decisions::from([

2    'call_abc' => true,

3])->rejectRemaining('Not approved.');

4 

5$response = (new FileAssistant)

6    ->continue($conversationId, as: $user)

7    ->prompt($decisions);
```

A rejection with a result, such as `Decision::reject('Not approved.')`, is returned to the model so it may continue responding. A rejection without a result stops the generation loop after recording the rejection.

Tool approval is supported by the `prompt`, `stream`, `queue`, `broadcast`, `broadcastNow`, and `broadcastOnQueue` methods.

During streaming and broadcasting, a pause is represented by a `tool_approval_request` event. When using the [Vercel AI SDK stream protocol](#streaming-using-the-vercel-ai-sdk-protocol), approval requests and results are emitted using the protocol's native tool approval parts.

For queued agents, the resulting response is passed to the `then` callback, and Laravel also dispatches a `ToolApprovalRequested` event.

Laravel stores the result of an approved tool before asking the model to continue. If generation then fails, the approval has already been resolved. Continue the conversation with a normal text prompt instead of submitting the same approval decisions again.

### [Complete Approval Flow](#complete-approval-flow)

The following routes demonstrate a complete approval flow. The `GET` route returns the chat screen, while the `POST` route accepts either a new text prompt or approval decisions from the chat screen. This example assumes the application's `User` model uses the `HasConversations` trait:

```
 1use App\Ai\Agents\FileAssistant;

 2use Illuminate\Http\Request;

 3use Illuminate\Support\Facades\Gate;

 4use Illuminate\Support\Facades\Route;

 5use Illuminate\Validation\Rule;

 6use Laravel\Ai\Approvals\Decision;

 7use Laravel\Ai\Approvals\Decisions;

 8use Laravel\Ai\Models\Conversation;

 9 

10Route::get('/chat/{conversation}', function (Request $request, Conversation $conversation) {

11    Gate::authorize('view', $conversation);

12 

13    return view('chat', [

14        'conversation' => $conversation,

15    ]);

16})->middleware('auth');

17 

18Route::post('/chat/{conversation}', function (Request $request, Conversation $conversation) {

19    Gate::authorize('view', $conversation);

20 

21    $validated = $request->validate([

22        'message' => ['nullable', 'string', 'required_without:decisions', 'prohibited_with:decisions'],

23        'decisions' => ['nullable', 'array', 'required_without:message', 'prohibited_with:message'],

24        'decisions.*.action' => ['required_with:decisions', Rule::in(['approve', 'reject'])],

25        'decisions.*.result' => ['nullable', 'string'],

26    ]);

27 

28    $prompt = isset($validated['decisions'])

29        ? Decisions::from($validated->collect('decisions')->map(

30            fn (array $decision) => match ($decision['action']) {

31                'approve' => Decision::approve(),

32                'reject' => Decision::reject($decision['result'] ?? null),

33            }

34        )->all())

35        : $validated['message'];

36 

37    $response = (new FileAssistant)

38        ->continue($conversation->id, as: $request->user())

39        ->prompt($prompt);

40 

41    return [

42        'conversation_id' => $response->conversationId,

43        'status' => $response->hasPendingApprovals() ? 'awaiting_approval' : 'complete',

44        'message' => $response->text,

45        'approvals' => $response->pendingApprovals,

46    ];

47})->middleware('auth');
```

When the response status is `awaiting_approval`, the chat screen should render the pending approvals and submit the user's choices to the same endpoint using the tool call ID as each decision's key:

```
 1{

 2    "decisions": {

 3        "call_abc": {

 4            "action": "approve"

 5        },

 6        "call_def": {

 7            "action": "reject",

 8            "result": "The invoice must be retained."

 9        }

10    }

11}
```

For a normal chat message, the screen may instead submit a `message` value:

```
1{

2    "message": "Delete the old invoice."

3}
```

## [Images](#images)

The `Laravel\Ai\Image` class may be used to generate images using the `openai`, `gemini`, or `xai` providers:

```
1use Laravel\Ai\Image;

2 

3$image = Image::of('A donut sitting on the kitchen counter')->generate();

4 

5$rawContent = (string) $image;
```

The `square`, `portrait`, and `landscape` methods may be used to control the aspect ratio of the image, while the `quality` method may be used to guide the model on final image quality (`high`, `medium`, `low`). The `timeout` method may be used to specify the HTTP timeout in seconds:

```
1use Laravel\Ai\Image;

2 

3$image = Image::of('A donut sitting on the kitchen counter')

4    ->quality('high')

5    ->landscape()

6    ->timeout(120)

7    ->generate();
```

You may attach reference images using the `attachments` method:

```
 1use Laravel\Ai\Files;

 2use Laravel\Ai\Image;

 3 

 4$image = Image::of('Update this photo of me to be in the style of an impressionist painting.')

 5    ->attachments([

 6        Files\Image::fromStorage('photo.jpg'),

 7        // Files\Image::fromPath('/home/laravel/photo.jpg'),

 8        // Files\Image::fromUrl('https://example.com/photo.jpg'),

 9        // $request->file('photo'),

10    ])

11    ->landscape()

12    ->generate();
```

Generated images may be easily stored on the default disk configured in your application's `config/filesystems.php` configuration file:

```
1$image = Image::of('A donut sitting on the kitchen counter');

2 

3$path = $image->store();

4$path = $image->storeAs('image.jpg');

5$path = $image->storePublicly();

6$path = $image->storePubliclyAs('image.jpg');
```

Image generation may also be queued:

```
 1use Laravel\Ai\Image;

 2use Laravel\Ai\Responses\ImageResponse;

 3 

 4Image::of('A donut sitting on the kitchen counter')

 5    ->portrait()

 6    ->queue()

 7    ->then(function (ImageResponse $image) {

 8        $path = $image->store();

 9 

10        // ...

11    });
```

## [Audio](#audio)

The `Laravel\Ai\Audio` class may be used to generate audio from the given text:

```
1use Laravel\Ai\Audio;

2 

3$audio = Audio::of('I love coding with Laravel.')->generate();

4 

5$rawContent = (string) $audio;
```

You may also generate audio from a string using the `toAudio` method available via Laravel's `Stringable` class:

```
1use Illuminate\Support\Str;

2 

3$audio = Str::of('I love coding with Laravel.')->toAudio();
```

The `male`, `female`, and `voice` methods may be used to determine the voice of the generated audio:

```
1$audio = Audio::of('I love coding with Laravel.')

2    ->female()

3    ->generate();

4 

5$audio = Audio::of('I love coding with Laravel.')

6    ->voice('voice-id-or-name')

7    ->generate();
```

Similarly, the `instructions` method may be used to dynamically coach the model on how the generated audio should sound:

```
1$audio = Audio::of('I love coding with Laravel.')

2    ->female()

3    ->instructions('Said like a pirate')

4    ->generate();
```

Generated audio may be easily stored on the default disk configured in your application's `config/filesystems.php` configuration file:

```
1$audio = Audio::of('I love coding with Laravel.')->generate();

2 

3$path = $audio->store();

4$path = $audio->storeAs('audio.mp3');

5$path = $audio->storePublicly();

6$path = $audio->storePubliclyAs('audio.mp3');
```

Audio generation may also be queued:

```
 1use Laravel\Ai\Audio;

 2use Laravel\Ai\Responses\AudioResponse;

 3 

 4Audio::of('I love coding with Laravel.')

 5    ->queue()

 6    ->then(function (AudioResponse $audio) {

 7        $path = $audio->store();

 8 

 9        // ...

10    });
```

## [Transcriptions](#transcription)

The `Laravel\Ai\Transcription` class may be used to generate a transcript of the given audio:

```
1use Laravel\Ai\Transcription;

2 

3$transcript = Transcription::fromPath('/home/laravel/audio.mp3')->generate();

4$transcript = Transcription::fromStorage('audio.mp3')->generate();

5$transcript = Transcription::fromUpload($request->file('audio'))->generate();

6 

7return (string) $transcript;
```

The `diarize` method may be used to indicate you would like the response to include the diarized transcript in addition to the raw text transcript, allowing you to access the segmented transcript by speaker:

```
1$transcript = Transcription::fromStorage('audio.mp3')

2    ->diarize()

3    ->generate();
```

Transcription generation may also be queued:

```
1use Laravel\Ai\Transcription;

2use Laravel\Ai\Responses\TranscriptionResponse;

3 

4Transcription::fromStorage('audio.mp3')

5    ->queue()

6    ->then(function (TranscriptionResponse $transcript) {

7        // ...

8    });
```

## [Text Summarization](#text-summarization)

You may summarize text using the `summarize` method available via Laravel's `Stringable` class. By default, the summary will contain no more than three sentences and will be generated using the configured provider's cheapest text model:

```
1use Illuminate\Support\Str;

2 

3$summary = Str::of($article)->summarize();
```

You may specify the maximum number of sentences, provider, model, and timeout used to generate the summary. The `Str` class also offers a static version of the method:

```
 1use Laravel\Ai\Enums\Lab;

 2 

 3$summary = Str::of($article)->summarize(

 4    sentences: 4,

 5    provider: Lab::Anthropic,

 6    model: 'claude-sonnet-5',

 7    timeout: 30,

 8);

 9 

10$summary = Str::summarize($article, sentences: 4);
```

## [Embeddings](#embeddings)

You may easily generate vector embeddings for any given string using the new `toEmbeddings` method available via Laravel's `Stringable` class:

```
1use Illuminate\Support\Str;

2 

3$embeddings = Str::of('Napa Valley has great wine.')->toEmbeddings();
```

Alternatively, you may use the `Embeddings` class to generate embeddings for multiple inputs at once:

```
1use Laravel\Ai\Embeddings;

2 

3$response = Embeddings::for([

4    'Napa Valley has great wine.',

5    'Laravel is a PHP framework.',

6])->generate();

7 

8$response->embeddings; // [[0.123, 0.456, ...], [0.789, 0.012, ...]]
```

You may specify the dimensions and provider for the embeddings:

```
1$response = Embeddings::for(['Napa Valley has great wine.'])

2    ->dimensions(1536)

3    ->generate(Lab::OpenAI, 'text-embedding-3-small');
```

### [Multimodal Embeddings](#multimodal-embeddings)

In addition to strings, the `Embeddings::for` method accepts image, audio, document, and video inputs, allowing you to generate embeddings for non-text content. Gemini supports image, audio, document, and video embeddings, while VoyageAI supports image and video embeddings:

```
 1use Laravel\Ai\Embeddings;

 2use Laravel\Ai\Enums\Lab;

 3use Laravel\Ai\Files\Image;

 4use Laravel\Ai\Files\Video;

 5 

 6$response = Embeddings::for([

 7    'A vineyard at sunset.',

 8    Image::fromStorage('vineyard.jpg'),

 9    Video::fromPath('/home/laravel/tour.mp4'),

10])->generate(Lab::Gemini);
```

Multimodal inputs use the same [file classes used for attachments](#attachments). These files may be created from a local path, a filesystem disk, a remote URL, or Base64-encoded content. Images, documents, and videos may also be created from uploaded files, while documents may be created from raw string content:

```
 1use Laravel\Ai\Files\Audio;

 2use Laravel\Ai\Files\Document;

 3use Laravel\Ai\Files\Image;

 4use Laravel\Ai\Files\Video;

 5 

 6Image::fromPath('/home/laravel/photo.jpg');

 7Image::fromStorage('photo.jpg');

 8Image::fromUpload($request->file('photo'));

 9 

10Audio::fromPath('/home/laravel/clip.mp3');

11Audio::fromStorage('clip.mp3');

12Audio::fromUpload($request->file('clip.mp3'));

13 

14Video::fromPath('/home/laravel/video.mp4');

15Video::fromStorage('video.mp4');

16Video::fromUpload($request->file('video'));

17 

18Document::fromUrl('https://example.com/report.pdf');

19Document::fromString('Laravel is a PHP framework.', 'text/plain');

20Document::fromUpload($request->file('report'));
```

VoyageAI does not allow remote URL media and Base64-encoded media to be mixed in a single request. Local, stored, and uploaded files are sent as Base64-encoded content, and text inputs may be combined with either media source. Consult your provider's documentation to determine which multimodal models and inputs are available.

### [Querying Embeddings](#querying-embeddings)

Once you have generated embeddings, you will typically store them in a `vector` column in your database for later querying. Laravel provides native support for vector columns on PostgreSQL via the `pgvector` extension. To get started, define a `vector` column in your migration, specifying the number of dimensions:

```
1Schema::ensureVectorExtensionExists();

2 

3Schema::create('documents', function (Blueprint $table) {

4    $table->id();

5    $table->string('title');

6    $table->text('content');

7    $table->vector('embedding', dimensions: 1536);

8    $table->timestamps();

9});
```

You may also add a vector index to speed up similarity searches. When calling `index` on a vector column, Laravel will automatically create an HNSW index with cosine distance:

```
1$table->vector('embedding', dimensions: 1536)->index();
```

On your Eloquent model, you should cast the vector column to an `array`:

```
1protected function casts(): array

2{

3    return [

4        'embedding' => 'array',

5    ];

6}
```

To query for similar records, use the `whereVectorSimilarTo` method. This method filters results by a minimum cosine similarity (between `0.0` and `1.0`, where `1.0` is identical) and orders the results by similarity:

```
1use App\Models\Document;

2 

3$documents = Document::query()

4    ->whereVectorSimilarTo('embedding', $queryEmbedding, minSimilarity: 0.4)

5    ->limit(10)

6    ->get();
```

The `$queryEmbedding` may be an array of floats or a plain string. When a string is given, Laravel will automatically generate embeddings for it:

```
1$documents = Document::query()

2    ->whereVectorSimilarTo('embedding', 'best wineries in Napa Valley')

3    ->limit(10)

4    ->get();
```

If you need more control, you may use the lower-level `whereVectorDistanceLessThan`, `selectVectorDistance`, and `orderByVectorDistance` methods independently:

```
1$documents = Document::query()

2    ->select('*')

3    ->selectVectorDistance('embedding', $queryEmbedding, as: 'distance')

4    ->whereVectorDistanceLessThan('embedding', $queryEmbedding, maxDistance: 0.3)

5    ->orderByVectorDistance('embedding', $queryEmbedding)

6    ->limit(10)

7    ->get();
```

If you would like to give an agent the ability to perform similarity searches as a tool, check out the [Similarity Search](#similarity-search) tool documentation.

Vector queries are currently only supported on PostgreSQL connections using the `pgvector` extension.

### [Caching Embeddings](#caching-embeddings)

Embedding generation can be cached to avoid redundant API calls for identical inputs. To enable caching, set the `ai.caching.embeddings.cache` configuration option to `true`:

```
1'caching' => [

2    'embeddings' => [

3        'cache' => true,

4        'store' => env('CACHE_STORE', 'database'),

5        // ...

6    ],

7],
```

When caching is enabled, embeddings are cached for 30 days. The cache key is based on the provider, model, dimensions, and input content, ensuring that identical requests return cached results while different configurations generate fresh embeddings.

You may also enable caching for a specific request using the `cache` method, even when global caching is disabled:

```
1$response = Embeddings::for(['Napa Valley has great wine.'])

2    ->cache()

3    ->generate();
```

You may specify a custom cache duration in seconds:

```
1$response = Embeddings::for(['Napa Valley has great wine.'])

2    ->cache(seconds: 3600) // Cache for 1 hour

3    ->generate();
```

The `toEmbeddings` Stringable method also accepts a `cache` argument:

```
1// Cache with default duration...

2$embeddings = Str::of('Napa Valley has great wine.')->toEmbeddings(cache: true);

3 

4// Cache for a specific duration...

5$embeddings = Str::of('Napa Valley has great wine.')->toEmbeddings(cache: 3600);
```

## [Reranking](#reranking)

Reranking allows you to reorder a list of documents based on their relevance to a given query. This is useful for improving search results by using semantic understanding:

The `Laravel\Ai\Reranking` class may be used to rerank documents:

```
 1use Laravel\Ai\Reranking;

 2 

 3$response = Reranking::of([

 4    'Django is a Python web framework.',

 5    'Laravel is a PHP web application framework.',

 6    'React is a JavaScript library for building user interfaces.',

 7])->rerank('PHP frameworks');

 8 

 9// Access the top result...

10$response->first()->document; // "Laravel is a PHP web application framework."

11$response->first()->score;    // 0.95

12$response->first()->index;    // 1 (original position)
```

The `limit` method may be used to restrict the number of results returned:

```
1$response = Reranking::of($documents)

2    ->limit(5)

3    ->rerank('search query');
```

### [Reranking Collections](#reranking-collections)

For convenience, Laravel collections may be reranked using the `rerank` macro. The first argument specifies which field(s) to use for reranking, and the second argument is the query:

```
 1// Rerank by a single field...

 2$posts = Post::all()

 3    ->rerank('body', 'Laravel tutorials');

 4 

 5// Rerank by multiple fields (sent as JSON)...

 6$reranked = $posts->rerank(['title', 'body'], 'Laravel tutorials');

 7 

 8// Rerank using a closure to build the document...

 9$reranked = $posts->rerank(

10    fn ($post) => $post->title.': '.$post->body,

11    'Laravel tutorials'

12);
```

You may also limit the number of results and specify a provider:

```
1$reranked = $posts->rerank(

2    by: 'content',

3    query: 'Laravel tutorials',

4    limit: 10,

5    provider: Lab::Cohere

6);
```

## [Files](#files)

The `Laravel\Ai\Files` class or the individual file classes may be used to store files with your AI provider for later use in conversations. This is useful for large documents or files you want to reference multiple times without re-uploading:

```
 1use Laravel\Ai\Files\Document;

 2use Laravel\Ai\Files\Image;

 3 

 4// Store a file from a local path...

 5$response = Document::fromPath('/home/laravel/document.pdf')->put();

 6$response = Image::fromPath('/home/laravel/photo.jpg')->put();

 7 

 8// Store a file that is stored on a filesystem disk...

 9$response = Document::fromStorage('document.pdf', disk: 'local')->put();

10$response = Image::fromStorage('photo.jpg', disk: 'local')->put();

11 

12// Store a file that is stored on a remote URL...

13$response = Document::fromUrl('https://example.com/document.pdf')->put();

14$response = Image::fromUrl('https://example.com/photo.jpg')->put();

15 

16return $response->id;
```

You may also store raw content or uploaded files:

```
1use Laravel\Ai\Files;

2use Laravel\Ai\Files\Document;

3 

4// Store raw content...

5$stored = Document::fromString('Hello, World!', 'text/plain')->put();

6 

7// Store an uploaded file...

8$stored = Document::fromUpload($request->file('document'))->put();
```

Once a file has been stored, you may reference the file when generating text via agents instead of re-uploading the file:

```
1use App\Ai\Agents\SalesCoach;

2use Laravel\Ai\Files;

3 

4$response = (new SalesCoach)->prompt(

5    'Analyze the attached sales transcript...'

6    attachments: [

7        Files\Document::fromId('file-id') // Attach a stored document...

8    ]

9);
```

To retrieve a previously stored file, use the `get` method on a file instance:

```
1use Laravel\Ai\Files\Document;

2 

3$file = Document::fromId('file-id')->get();

4 

5$file->id;

6$file->mimeType();
```

To delete a file from the provider, use the `delete` method:

```
1Document::fromId('file-id')->delete();
```

By default, the `Files` class uses the default AI provider configured in your application's `config/ai.php` configuration file. For most operations, you may specify a different provider using the `provider` argument:

```
1$response = Document::fromPath(

2    '/home/laravel/document.pdf'

3)->put(provider: Lab::Anthropic);
```

You may pass provider-specific upload options using the `withProviderOptions` method. For example, you may set OpenAI's file `purpose`:

```
1use Laravel\Ai\Files\Document;

2 

3$response = Document::fromPath('/home/laravel/knowledge.txt')

4    ->withProviderOptions(['purpose' => 'assistants'])

5    ->put();
```

To scope options per provider, pass a closure that receives the current provider:

```
1use Laravel\Ai\Enums\Lab;

2use Laravel\Ai\Files\Document;

3 

4$response = Document::fromPath('/home/laravel/training.jsonl')

5    ->withProviderOptions(fn (Lab|string $provider) => match ($provider) {

6        Lab::OpenAI => ['purpose' => 'fine-tune'],

7        default => [],

8    })

9    ->put();
```

### [Using Stored Files in Conversations](#using-stored-files-in-conversations)

Once a file has been stored with a provider, you may reference it in agent conversations using the `fromId` method on the `Document` or `Image` classes:

```
 1use App\Ai\Agents\DocumentAnalyzer;

 2use Laravel\Ai\Files;

 3use Laravel\Ai\Files\Document;

 4 

 5$stored = Document::fromPath('/path/to/report.pdf')->put();

 6 

 7$response = (new DocumentAnalyzer)->prompt(

 8    'Summarize this document.',

 9    attachments: [

10        Document::fromId($stored->id),

11    ],

12);
```

Similarly, stored images may be referenced using the `Image` class:

```
 1use Laravel\Ai\Files;

 2use Laravel\Ai\Files\Image;

 3 

 4$stored = Image::fromPath('/path/to/photo.jpg')->put();

 5 

 6$response = (new ImageAnalyzer)->prompt(

 7    'What is in this image?',

 8    attachments: [

 9        Image::fromId($stored->id),

10    ],

11);
```

## [Vector Stores](#vector-stores)

Vector stores allow you to create searchable collections of files that can be used for retrieval-augmented generation (RAG). The `Laravel\Ai\Stores` class provides methods for creating, retrieving, and deleting vector stores:

```
 1use Laravel\Ai\Stores;

 2 

 3// Create a new vector store...

 4$store = Stores::create('Knowledge Base');

 5 

 6// Create a store with additional options...

 7$store = Stores::create(

 8    name: 'Knowledge Base',

 9    description: 'Documentation and reference materials.',

10    expiresWhenIdleFor: days(30),

11);

12 

13return $store->id;
```

To retrieve an existing vector store by its ID, use the `get` method:

```
1use Laravel\Ai\Stores;

2 

3$store = Stores::get('store_id');

4 

5$store->id;

6$store->name;

7$store->fileCounts;

8$store->ready;
```

To delete a vector store, use the `delete` method on the `Stores` class or the store instance:

```
1use Laravel\Ai\Stores;

2 

3// Delete by ID...

4Stores::delete('store_id');

5 

6// Or delete via a store instance...

7$store = Stores::get('store_id');

8 

9$store->delete();
```

### [Adding Files to Stores](#adding-files-to-stores)

Once you have a vector store, you may add [files](#files) to it using the `add` method. Files added to a store are automatically indexed for semantic searching using the [file search provider tool](#file-search):

```
 1use Laravel\Ai\Files\Document;

 2use Laravel\Ai\Stores;

 3 

 4$store = Stores::get('store_id');

 5 

 6// Add a file that has already been stored with the provider...

 7$document = $store->add('file_id');

 8$document = $store->add(Document::fromId('file_id'));

 9 

10// Or, store and add a file in one step...

11$document = $store->add(Document::fromPath('/path/to/document.pdf'));

12$document = $store->add(Document::fromStorage('manual.pdf'));

13$document = $store->add($request->file('document'));

14 

15$document->id;

16$document->fileId;
```

Typically, when adding previously stored files to vector stores, the returned document ID will match the file's previously assigned ID; however, some vector storage providers may return a new, different "document ID". Therefore, it's recommended that you always store both IDs in your database for future reference.

You may attach metadata to files when adding them to a store. This metadata can later be used to filter search results when using the [file search provider tool](#file-search):

```
1$store->add(Document::fromPath('/path/to/document.pdf'), metadata: [

2    'author' => 'Taylor Otwell',

3    'department' => 'Engineering',

4    'year' => 2026,

5]);
```

To remove a file from a store, use the `remove` method:

```
1$store->remove('file_id');
```

Removing a file from a vector store does not remove it from the provider's [file storage](#files). To remove a file from the vector store and delete it permanently from file storage, use the `deleteFile` argument:

```
1$store->remove('file_abc123', deleteFile: true);
```

## [Failover](#failover)

When prompting or generating other media, you may provide an array of providers / models to automatically failover to a backup provider / model if a service interruption or rate limit is encountered on the primary provider:

```
 1use App\Ai\Agents\SalesCoach;

 2use Laravel\Ai\Enums\Lab;

 3use Laravel\Ai\Image;

 4 

 5$response = (new SalesCoach)->prompt(

 6    'Analyze this sales transcript...',

 7    provider: [Lab::OpenAI, Lab::Anthropic],

 8);

 9 

10$image = Image::of('A donut sitting on the kitchen counter')

11    ->generate(provider: [Lab::Gemini, Lab::xAI]);
```

Failover only occurs when a `FailoverableException` is thrown — such as a rate limit (`RateLimitedException`), an overloaded or unavailable provider (`ProviderOverloadedException`), or insufficient credits (`InsufficientCreditsException`). Ordinary errors, like a validation or bad request error, will not trigger failover.

When you pass a plain list of providers, such as `[Lab::OpenAI, Lab::Anthropic]`, each provider uses its default model. To specify a particular model for each provider in the failover chain, pass an associative array keyed by the provider, using the `Lab` enum's `value` as the key (enum cases cannot be used directly as PHP array keys):

```
1use Laravel\Ai\Enums\Lab;

2 

3$response = (new SalesCoach)->prompt(

4    'Analyze this sales transcript...',

5    provider: [

6        Lab::Gemini->value => 'gemini-3-flash-preview',

7        Lab::DeepSeek->value => 'deepseek-v4-pro',

8    ],

9);
```

## [Testing](#testing)

### [Agents](#testing-agents)

To fake an agent's responses during tests, call the `fake` method on the agent class. You may optionally provide an array of responses or a closure:

```
 1use App\Ai\Agents\SalesCoach;

 2use Laravel\Ai\Prompts\AgentPrompt;

 3 

 4// Automatically generate a fixed response for every prompt...

 5SalesCoach::fake();

 6 

 7// Provide a list of prompt responses...

 8SalesCoach::fake([

 9    'First response',

10    'Second response',

11]);

12 

13// Dynamically handle prompt responses based on the incoming prompt...

14SalesCoach::fake(function (AgentPrompt $prompt) {

15    return 'Response for: '.$prompt->prompt;

16});
```

When faking an agent that returns structured output, you may provide arrays as responses. The agent will return a structured response containing the given data:

```
1SalesCoach::fake([

2    ['score' => 87],

3]);
```

You may also fake a response that is awaiting tool approval:

```
 1use Laravel\Ai\Approvals\PendingApproval;

 2use Laravel\Ai\Responses\AgentResponse;

 3 

 4FileAssistant::fake([

 5    AgentResponse::fakeWithPendingApprovals([

 6        new PendingApproval(

 7            id: 'call_abc',

 8            tool: 'DeleteFile',

 9            arguments: ['path' => 'invoice.pdf'],

10            reason: 'This will permanently delete a file.',

11        ),

12    ]),

13]);

14 

15$response = (new FileAssistant)->prompt('Delete the invoice.');

16 

17$response->hasPendingApprovals(); // true
```

When `Agent::fake()` is invoked on an agent that returns structured output and fake output was not explicitly provided, Laravel will automatically generate fake data that matches your agent's defined output schema.

After prompting the agent, you may make assertions about the prompts that were received:

```
 1use Laravel\Ai\Prompts\AgentPrompt;

 2 

 3SalesCoach::assertPrompted('Analyze this...');

 4 

 5SalesCoach::assertPrompted(function (AgentPrompt $prompt) {

 6    return $prompt->contains('Analyze');

 7});

 8 

 9SalesCoach::assertNotPrompted('Missing prompt');

10 

11SalesCoach::assertNeverPrompted();
```

When asserting an approval continuation, you may inspect the prompt's approval decisions:

```
 1use Laravel\Ai\Approvals\Decisions;

 2use Laravel\Ai\Prompts\AgentPrompt;

 3 

 4FileAssistant::fake();

 5 

 6(new FileAssistant)->prompt(Decisions::from([

 7    'call_abc' => true,

 8]));

 9 

10FileAssistant::assertPrompted(function (AgentPrompt $prompt) {

11    return $prompt->hasApprovalDecisions()

12        && $prompt->approvalDecisions->get('call_abc')->isApproved();

13});
```

For queued agent invocations, use the queued assertion methods:

```
 1use Laravel\Ai\QueuedAgentPrompt;

 2 

 3SalesCoach::assertQueued('Analyze this...');

 4 

 5SalesCoach::assertQueued(function (QueuedAgentPrompt $prompt) {

 6    return $prompt->contains('Analyze');

 7});

 8 

 9SalesCoach::assertNotQueued('Missing prompt');

10 

11SalesCoach::assertNeverQueued();
```

To ensure all agent invocations have a corresponding fake response, you may use `preventStrayPrompts`. If an agent is invoked without a defined fake response, an exception will be thrown:

```
1SalesCoach::fake()->preventStrayPrompts();
```

### [Images](#testing-images)

Image generations may be faked by invoking the `fake` method on the `Image` class. Once image has been faked, various assertions may be performed against the recorded image generation prompts:

```
 1use Laravel\Ai\Image;

 2use Laravel\Ai\Prompts\ImagePrompt;

 3use Laravel\Ai\Prompts\QueuedImagePrompt;

 4 

 5// Automatically generate a fixed response for every prompt...

 6Image::fake();

 7 

 8// Provide a list of prompt responses...

 9Image::fake([

10    base64_encode($firstImage),

11    base64_encode($secondImage),

12]);

13 

14// Dynamically handle prompt responses based on the incoming prompt...

15Image::fake(function (ImagePrompt $prompt) {

16    return base64_encode('...');

17});
```

After generating images, you may make assertions about the prompts that were received:

```
1Image::assertGenerated(function (ImagePrompt $prompt) {

2    return $prompt->contains('sunset') && $prompt->isLandscape();

3});

4 

5Image::assertNotGenerated('Missing prompt');

6 

7Image::assertNothingGenerated();
```

For queued image generations, use the queued assertion methods:

```
1Image::assertQueued(

2    fn (QueuedImagePrompt $prompt) => $prompt->contains('sunset')

3);

4 

5Image::assertNotQueued('Missing prompt');

6 

7Image::assertNothingQueued();
```

To ensure all image generations have a corresponding fake response, you may use `preventStrayImages`. If an image is generated without a defined fake response, an exception will be thrown:

```
1Image::fake()->preventStrayImages();
```

### [Audio](#testing-audio)

Audio generations may be faked by invoking the `fake` method on the `Audio` class. Once audio has been faked, various assertions may be performed against the recorded audio generation prompts:

```
 1use Laravel\Ai\Audio;

 2use Laravel\Ai\Prompts\AudioPrompt;

 3use Laravel\Ai\Prompts\QueuedAudioPrompt;

 4 

 5// Automatically generate a fixed response for every prompt...

 6Audio::fake();

 7 

 8// Provide a list of prompt responses...

 9Audio::fake([

10    base64_encode($firstAudio),

11    base64_encode($secondAudio),

12]);

13 

14// Dynamically handle prompt responses based on the incoming prompt...

15Audio::fake(function (AudioPrompt $prompt) {

16    return base64_encode('...');

17});
```

After generating audio, you may make assertions about the prompts that were received:

```
1Audio::assertGenerated(function (AudioPrompt $prompt) {

2    return $prompt->contains('Hello') && $prompt->isFemale();

3});

4 

5Audio::assertNotGenerated('Missing prompt');

6 

7Audio::assertNothingGenerated();
```

For queued audio generations, use the queued assertion methods:

```
1Audio::assertQueued(

2    fn (QueuedAudioPrompt $prompt) => $prompt->contains('Hello')

3);

4 

5Audio::assertNotQueued('Missing prompt');

6 

7Audio::assertNothingQueued();
```

To ensure all audio generations have a corresponding fake response, you may use `preventStrayAudio`. If audio is generated without a defined fake response, an exception will be thrown:

```
1Audio::fake()->preventStrayAudio();
```

### [Transcriptions](#testing-transcriptions)

Transcription generations may be faked by invoking the `fake` method on the `Transcription` class. Once transcription has been faked, various assertions may be performed against the recorded transcription generation prompts:

```
 1use Laravel\Ai\Transcription;

 2use Laravel\Ai\Prompts\TranscriptionPrompt;

 3use Laravel\Ai\Prompts\QueuedTranscriptionPrompt;

 4 

 5// Automatically generate a fixed response for every prompt...

 6Transcription::fake();

 7 

 8// Provide a list of prompt responses...

 9Transcription::fake([

10    'First transcription text.',

11    'Second transcription text.',

12]);

13 

14// Dynamically handle prompt responses based on the incoming prompt...

15Transcription::fake(function (TranscriptionPrompt $prompt) {

16    return 'Transcribed text...';

17});
```

After generating transcriptions, you may make assertions about the prompts that were received:

```
1Transcription::assertGenerated(function (TranscriptionPrompt $prompt) {

2    return $prompt->language === 'en' && $prompt->isDiarized();

3});

4 

5Transcription::assertNotGenerated(

6    fn (TranscriptionPrompt $prompt) => $prompt->language === 'fr'

7);

8 

9Transcription::assertNothingGenerated();
```

For queued transcription generations, use the queued assertion methods:

```
1Transcription::assertQueued(

2    fn (QueuedTranscriptionPrompt $prompt) => $prompt->isDiarized()

3);

4 

5Transcription::assertNotQueued(

6    fn (QueuedTranscriptionPrompt $prompt) => $prompt->language === 'fr'

7);

8 

9Transcription::assertNothingQueued();
```

To ensure all transcription generations have a corresponding fake response, you may use `preventStrayTranscriptions`. If a transcription is generated without a defined fake response, an exception will be thrown:

```
1Transcription::fake()->preventStrayTranscriptions();
```

### [Embeddings](#testing-embeddings)

Embeddings generations may be faked by invoking the `fake` method on the `Embeddings` class. Once embeddings has been faked, various assertions may be performed against the recorded embeddings generation prompts:

```
 1use Laravel\Ai\Embeddings;

 2use Laravel\Ai\Prompts\EmbeddingsPrompt;

 3use Laravel\Ai\Prompts\QueuedEmbeddingsPrompt;

 4 

 5// Automatically generate fake embeddings of the proper dimensions for every prompt...

 6Embeddings::fake();

 7 

 8// Provide a list of prompt responses...

 9Embeddings::fake([

10    [$firstEmbeddingVector],

11    [$secondEmbeddingVector],

12]);

13 

14// Dynamically handle prompt responses based on the incoming prompt...

15Embeddings::fake(function (EmbeddingsPrompt $prompt) {

16    return array_map(

17        fn () => Embeddings::fakeEmbedding($prompt->dimensions),

18        $prompt->inputs

19    );

20});
```

After generating embeddings, you may make assertions about the prompts that were received:

```
1Embeddings::assertGenerated(function (EmbeddingsPrompt $prompt) {

2    return $prompt->contains('Laravel') && $prompt->dimensions === 1536;

3});

4 

5Embeddings::assertNotGenerated(

6    fn (EmbeddingsPrompt $prompt) => $prompt->contains('Other')

7);

8 

9Embeddings::assertNothingGenerated();
```

For queued embeddings generations, use the queued assertion methods:

```
1Embeddings::assertQueued(

2    fn (QueuedEmbeddingsPrompt $prompt) => $prompt->contains('Laravel')

3);

4 

5Embeddings::assertNotQueued(

6    fn (QueuedEmbeddingsPrompt $prompt) => $prompt->contains('Other')

7);

8 

9Embeddings::assertNothingQueued();
```

To ensure all embeddings generations have a corresponding fake response, you may use `preventStrayEmbeddings`. If embeddings are generated without a defined fake response, an exception will be thrown:

```
1Embeddings::fake()->preventStrayEmbeddings();
```

### [Reranking](#testing-reranking)

Reranking operations may be faked by invoking the `fake` method on the `Reranking` class:

```
 1use Laravel\Ai\Reranking;

 2use Laravel\Ai\Prompts\RerankingPrompt;

 3use Laravel\Ai\Responses\Data\RankedDocument;

 4 

 5// Automatically generate a fake reranked responses...

 6Reranking::fake();

 7 

 8// Provide custom responses...

 9Reranking::fake([

10    [

11        new RankedDocument(index: 0, document: 'First', score: 0.95),

12        new RankedDocument(index: 1, document: 'Second', score: 0.80),

13    ],

14]);
```

After reranking, you may make assertions about the operations that were performed:

```
1Reranking::assertReranked(function (RerankingPrompt $prompt) {

2    return $prompt->contains('Laravel') && $prompt->limit === 5;

3});

4 

5Reranking::assertNotReranked(

6    fn (RerankingPrompt $prompt) => $prompt->contains('Django')

7);

8 

9Reranking::assertNothingReranked();
```

### [Files](#testing-files)

File operations may be faked by invoking the `fake` method on the `Files` class:

```
1use Laravel\Ai\Files;

2 

3Files::fake();
```

Once file operations have been faked, you may make assertions about the uploads and deletions that occurred:

```
 1use Laravel\Ai\Contracts\Files\StorableFile;

 2use Laravel\Ai\Files\Document;

 3 

 4// Store files...

 5Document::fromString('Hello, Laravel!', mimeType: 'text/plain')

 6    ->as('hello.txt')

 7    ->put();

 8 

 9// Make assertions...

10Files::assertStored(fn (StorableFile $file) =>

11    (string) $file === 'Hello, Laravel!' &&

12        $file->mimeType() === 'text/plain';

13);

14 

15Files::assertNotStored(fn (StorableFile $file) =>

16    (string) $file === 'Hello, World!'

17);

18 

19Files::assertNothingStored();
```

For asserting against file deletions, you may pass a file ID:

```
1Files::assertDeleted('file-id');

2Files::assertNotDeleted('file-id');

3Files::assertNothingDeleted();
```

### [Vector Stores](#testing-vector-stores)

Vector store operations may be faked by invoking the `fake` method on the `Stores` class. Faking stores will also fake [file operations](#files) automatically:

```
1use Laravel\Ai\Stores;

2 

3Stores::fake();
```

Once store operations have been faked, you may make assertions about the stores that were created or deleted:

```
 1use Laravel\Ai\Stores;

 2 

 3// Create store...

 4$store = Stores::create('Knowledge Base');

 5 

 6// Make assertions...

 7Stores::assertCreated('Knowledge Base');

 8 

 9Stores::assertCreated(fn (string $name, ?string $description) =>

10    $name === 'Knowledge Base'

11);

12 

13Stores::assertNotCreated('Other Store');

14 

15Stores::assertNothingCreated();
```

For asserting against store deletions, you may provide the store ID:

```
1Stores::assertDeleted('store_id');

2Stores::assertNotDeleted('other_store_id');

3Stores::assertNothingDeleted();
```

To assert files were added or removed from a store, use the assertion methods on a given `Store` instance:

```
 1Stores::fake();

 2 

 3$store = Stores::get('store_id');

 4 

 5// Add / remove files...

 6$store->add('added_id');

 7$store->remove('removed_id');

 8 

 9// Make assertions...

10$store->assertAdded('added_id');

11$store->assertRemoved('removed_id');

12 

13$store->assertNotAdded('other_file_id');

14$store->assertNotRemoved('other_file_id');
```

If a file is stored in the provider's [file storage](#files) and added to a vector store in the same request, you may not know the file's provider ID. In this case, you can pass a closure to the `assertAdded` method to assert against the content of the added file:

```
1use Laravel\Ai\Contracts\Files\StorableFile;

2use Laravel\Ai\Files\Document;

3 

4$store->add(Document::fromString('Hello, World!', 'text/plain')->as('hello.txt'));

5 

6$store->assertAdded(fn (StorableFile $file) => $file->name() === 'hello.txt');

7$store->assertAdded(fn (StorableFile $file) => $file->content() === 'Hello, World!');
```

## [Events](#events)

The Laravel AI SDK dispatches a variety of [events](/docs/13.x/events), including:

- `AddingFileToStore`
- `AgentPrompted`
- `AgentStreamed`
- `AudioGenerated`
- `CreatingStore`
- `EmbeddingsGenerated`
- `FileAddedToStore`
- `FileDeleted`
- `FileRemovedFromStore`
- `FileStored`
- `GeneratingAudio`
- `GeneratingEmbeddings`
- `GeneratingImage`
- `GeneratingTranscription`
- `ImageGenerated`
- `InvokingTool`
- `PromptingAgent`
- `RemovingFileFromStore`
- `Reranked`
- `Reranking`
- `StoreCreated`
- `StoringFile`
- `StreamingAgent`
- `ToolApprovalRequested`
- `ToolApprovalResolved`
- `ToolInvoked`
- `TranscriptionGenerated`

You can listen to any of these events to log or store AI SDK usage information.
