# Eloquent: Factories

- [Introduction](#introduction)
- [Defining Model Factories](#defining-model-factories)
  * [Generating Factories](#generating-factories)
  * [Factory States](#factory-states)
  * [Factory Callbacks](#factory-callbacks)
- [Creating Models Using Factories](#creating-models-using-factories)
  * [Instantiating Models](#instantiating-models)
  * [Persisting Models](#persisting-models)
  * [Sequences](#sequences)
- [Factory Relationships](#factory-relationships)
  * [Has Many Relationships](#has-many-relationships)
  * [Belongs To Relationships](#belongs-to-relationships)
  * [Many to Many Relationships](#many-to-many-relationships)
  * [Polymorphic Relationships](#polymorphic-relationships)
  * [Defining Relationships Within Factories](#defining-relationships-within-factories)
  * [Recycling an Existing Model for Relationships](#recycling-an-existing-model-for-relationships)

## [Introduction](#introduction)

When testing your application or seeding your database, you may need to insert a few records into your database. Instead of manually specifying the value of each column, Laravel allows you to define a set of default attributes for each of your [Eloquent models](/docs/13.x/eloquent) using model factories.

To see an example of how to write a factory, take a look at the `database/factories/UserFactory.php` file in your application. This factory is included with all new Laravel applications and contains the following factory definition:

```
 1namespace Database\Factories;

 2 

 3use Illuminate\Database\Eloquent\Factories\Factory;

 4use Illuminate\Support\Facades\Hash;

 5use Illuminate\Support\Str;

 6 

 7/**

 8 * @extends \Illuminate\Database\Eloquent\Factories\Factory<\App\Models\User>

 9 */

10class UserFactory extends Factory

11{

12    /**

13     * The current password being used by the factory.

14     */

15    protected static ?string $password;

16 

17    /**

18     * Define the model's default state.

19     *

20     * @return array<string, mixed>

21     */

22    public function definition(): array

23    {

24        return [

25            'name' => fake()->name(),

26            'email' => fake()->unique()->safeEmail(),

27            'email_verified_at' => now(),

28            'password' => static::$password ??= Hash::make('password'),

29            'remember_token' => Str::random(10),

30        ];

31    }

32 

33    /**

34     * Indicate that the model's email address should be unverified.

35     */

36    public function unverified(): static

37    {

38        return $this->state(fn (array $attributes) => [

39            'email_verified_at' => null,

40        ]);

41    }

42}
```

As you can see, in their most basic form, factories are classes that extend Laravel's base factory class and define a `definition` method. The `definition` method returns the default set of attribute values that should be applied when creating a model using the factory.

Via the `fake` helper, factories have access to the [Faker](https://github.com/FakerPHP/Faker) PHP library, which allows you to conveniently generate various kinds of random data for testing and seeding.

You can change your application's Faker locale by updating the `faker_locale` option in your `config/app.php` configuration file.

## [Defining Model Factories](#defining-model-factories)

### [Generating Factories](#generating-factories)

To create a factory, execute the `make:factory` [Artisan command](/docs/13.x/artisan):

```
1php artisan make:factory PostFactory
```

The new factory class will be placed in your `database/factories` directory.

#### [Model and Factory Discovery Conventions](#factory-and-model-discovery-conventions)

Once you have defined your factories, you may use the static `factory` method provided to your models by the `Illuminate\Database\Eloquent\Factories\HasFactory` trait in order to instantiate a factory instance for that model.

The `HasFactory` trait's `factory` method will use conventions to determine the proper factory for the model the trait is assigned to. Specifically, the method will look for a factory in the `Database\Factories` namespace that has a class name matching the model name and is suffixed with `Factory`. If these conventions do not apply to your particular application or factory, you may add the `UseFactory` attribute to the model to manually specify the model's factory:

```
1use Illuminate\Database\Eloquent\Attributes\UseFactory;

2use Database\Factories\Administration\FlightFactory;

3 

4#[UseFactory(FlightFactory::class)]

5class Flight extends Model

6{

7    // ...

8}
```

Alternatively, you may overwrite the `newFactory` method on your model to return an instance of the model's corresponding factory directly:

```
1use Database\Factories\Administration\FlightFactory;

2 

3/**

4 * Create a new factory instance for the model.

5 */

6protected static function newFactory()

7{

8    return FlightFactory::new();

9}
```

Then, use the `UseModel` attribute on the corresponding factory to specify the model:

```
1use App\Administration\Flight;

2use Illuminate\Database\Eloquent\Factories\Attributes\UseModel;

3use Illuminate\Database\Eloquent\Factories\Factory;

4 

5#[UseModel(Flight::class)]

6class FlightFactory extends Factory

7{

8    // ...

9}
```

### [Factory States](#factory-states)

State manipulation methods allow you to define discrete modifications that can be applied to your model factories in any combination. For example, your `Database\Factories\UserFactory` factory might contain a `suspended` state method that modifies one of its default attribute values.

State transformation methods typically call the `state` method provided by Laravel's base factory class. The `state` method accepts a closure which will receive the array of raw attributes defined for the factory and should return an array of attributes to modify:

```
 1use Illuminate\Database\Eloquent\Factories\Factory;

 2 

 3/**

 4 * Indicate that the user is suspended.

 5 */

 6public function suspended(): Factory

 7{

 8    return $this->state(function (array $attributes) {

 9        return [

10            'account_status' => 'suspended',

11        ];

12    });

13}
```

#### ["Trashed" State](#trashed-state)

If your Eloquent model can be [soft deleted](/docs/13.x/eloquent#soft-deleting), you may invoke the built-in `trashed` state method to indicate that the created model should already be "soft deleted". You do not need to manually define the `trashed` state as it is automatically available to all factories:

```
1use App\Models\User;

2 

3$user = User::factory()->trashed()->create();
```

### [Factory Callbacks](#factory-callbacks)

Factory callbacks are registered using the `afterMaking` and `afterCreating` methods and allow you to perform additional tasks after making or creating a model. You should register these callbacks by defining a `configure` method on your factory class. This method will be automatically called by Laravel when the factory is instantiated:

```
 1namespace Database\Factories;

 2 

 3use App\Models\User;

 4use Illuminate\Database\Eloquent\Factories\Factory;

 5 

 6class UserFactory extends Factory

 7{

 8    /**

 9     * Configure the model factory.

10     */

11    public function configure(): static

12    {

13        return $this->afterMaking(function (User $user) {

14            // ...

15        })->afterCreating(function (User $user) {

16            // ...

17        });

18    }

19 

20    // ...

21}
```

You may also register factory callbacks within state methods to perform additional tasks that are specific to a given state:

```
 1use App\Models\User;

 2use Illuminate\Database\Eloquent\Factories\Factory;

 3 

 4/**

 5 * Indicate that the user is suspended.

 6 */

 7public function suspended(): Factory

 8{

 9    return $this->state(function (array $attributes) {

10        return [

11            'account_status' => 'suspended',

12        ];

13    })->afterMaking(function (User $user) {

14        // ...

15    })->afterCreating(function (User $user) {

16        // ...

17    });

18}
```

## [Creating Models Using Factories](#creating-models-using-factories)

### [Instantiating Models](#instantiating-models)

Once you have defined your factories, you may use the static `factory` method provided to your models by the `Illuminate\Database\Eloquent\Factories\HasFactory` trait in order to instantiate a factory instance for that model. Let's take a look at a few examples of creating models. First, we'll use the `make` method to create models without persisting them to the database:

```
1use App\Models\User;

2 

3$user = User::factory()->make();
```

You may create a collection of many models using the `count` method:

```
1$users = User::factory()->count(3)->make();
```

#### [Applying States](#applying-states)

You may also apply any of your [states](#factory-states) to the models. If you would like to apply multiple state transformations to the models, you may simply call the state transformation methods directly:

```
1$users = User::factory()->count(5)->suspended()->make();
```

#### [Overriding Attributes](#overriding-attributes)

If you would like to override some of the default values of your models, you may pass an array of values to the `make` method. Only the specified attributes will be replaced while the rest of the attributes remain set to their default values as specified by the factory:

```
1$user = User::factory()->make([

2    'name' => 'Abigail Otwell',

3]);
```

Alternatively, the `state` method may be called directly on the factory instance to perform an inline state transformation:

```
1$user = User::factory()->state([

2    'name' => 'Abigail Otwell',

3])->make();
```

[Mass assignment protection](/docs/13.x/eloquent#mass-assignment) is automatically disabled when creating models using factories.

### [Persisting Models](#persisting-models)

The `create` method instantiates model instances and persists them to the database using Eloquent's `save` method:

```
1use App\Models\User;

2 

3// Create a single App\Models\User instance...

4$user = User::factory()->create();

5 

6// Create three App\Models\User instances...

7$users = User::factory()->count(3)->create();
```

You may override the factory's default model attributes by passing an array of attributes to the `create` method:

```
1$user = User::factory()->create([

2    'name' => 'Abigail',

3]);
```

### [Sequences](#sequences)

Sometimes you may wish to alternate the value of a given model attribute for each created model. You may accomplish this by defining a state transformation as a sequence. For example, you may wish to alternate the value of an `admin` column between `Y` and `N` for each created user:

```
 1use App\Models\User;

 2use Illuminate\Database\Eloquent\Factories\Sequence;

 3 

 4$users = User::factory()

 5    ->count(10)

 6    ->state(new Sequence(

 7        ['admin' => 'Y'],

 8        ['admin' => 'N'],

 9    ))

10    ->create();
```

In this example, five users will be created with an `admin` value of `Y` and five users will be created with an `admin` value of `N`.

If necessary, you may include a closure as a sequence value. The closure will be invoked each time the sequence needs a new value:

```
1use Illuminate\Database\Eloquent\Factories\Sequence;

2 

3$users = User::factory()

4    ->count(10)

5    ->state(new Sequence(

6        fn (Sequence $sequence) => ['role' => UserRoles::all()->random()],

7    ))

8    ->create();
```

Within a sequence closure, you may access the `$index` property on the sequence instance that is injected into the closure. The `$index` property contains the number of iterations through the sequence that have occurred thus far:

```
1$users = User::factory()

2    ->count(10)

3    ->state(new Sequence(

4        fn (Sequence $sequence) => ['name' => 'Name '.$sequence->index],

5    ))

6    ->create();
```

For convenience, sequences may also be applied using the `sequence` method, which simply invokes the `state` method internally. The `sequence` method accepts a closure or arrays of sequenced attributes:

```
1$users = User::factory()

2    ->count(2)

3    ->sequence(

4        ['name' => 'First User'],

5        ['name' => 'Second User'],

6    )

7    ->create();
```

## [Factory Relationships](#factory-relationships)

### [Has Many Relationships](#has-many-relationships)

Next, let's explore building Eloquent model relationships using Laravel's fluent factory methods. First, let's assume our application has an `App\Models\User` model and an `App\Models\Post` model. Also, let's assume that the `User` model defines a `hasMany` relationship with `Post`. We can create a user that has three posts using the `has` method provided by the Laravel's factories. The `has` method accepts a factory instance:

```
1use App\Models\Post;

2use App\Models\User;

3 

4$user = User::factory()

5    ->has(Post::factory()->count(3))

6    ->create();
```

By convention, when passing a `Post` model to the `has` method, Laravel will assume that the `User` model must have a `posts` method that defines the relationship. If necessary, you may explicitly specify the name of the relationship that you would like to manipulate:

```
1$user = User::factory()

2    ->has(Post::factory()->count(3), 'posts')

3    ->create();
```

Of course, you may perform state manipulations on the related models. In addition, you may pass a closure-based state transformation if your state change requires access to the parent model:

```
1$user = User::factory()

2    ->has(

3        Post::factory()

4            ->count(3)

5            ->state(function (array $attributes, User $user) {

6                return ['user_type' => $user->type];

7            })

8    )

9    ->create();
```

#### [Using Magic Methods](#has-many-relationships-using-magic-methods)

For convenience, you may use Laravel's magic factory relationship methods to build relationships. For example, the following example will use convention to determine that the related models should be created via a `posts` relationship method on the `User` model:

```
1$user = User::factory()

2    ->hasPosts(3)

3    ->create();
```

When using magic methods to create factory relationships, you may pass an array of attributes to override on the related models:

```
1$user = User::factory()

2    ->hasPosts(3, [

3        'published' => false,

4    ])

5    ->create();
```

You may also pass multiple attribute arrays to create related models with per-model state. Laravel will apply each array in sequence:

```
1$user = User::factory()

2    ->hasPosts(

3        ['title' => 'First Post'],

4        ['title' => 'Second Post'],

5        ['title' => 'Third Post'],

6    )

7    ->create();
```

You may provide a closure-based state transformation if your state change requires access to the parent model:

```
1$user = User::factory()

2    ->hasPosts(3, function (array $attributes, User $user) {

3        return ['user_type' => $user->type];

4    })

5    ->create();
```

### [Belongs To Relationships](#belongs-to-relationships)

Now that we have explored how to build "has many" relationships using factories, let's explore the inverse of the relationship. The `for` method may be used to define the parent model that factory created models belong to. For example, we can create three `App\Models\Post` model instances that belong to a single user:

```
1use App\Models\Post;

2use App\Models\User;

3 

4$posts = Post::factory()

5    ->count(3)

6    ->for(User::factory()->state([

7        'name' => 'Jessica Archer',

8    ]))

9    ->create();
```

If you already have a parent model instance that should be associated with the models you are creating, you may pass the model instance to the `for` method:

```
1$user = User::factory()->create();

2 

3$posts = Post::factory()

4    ->count(3)

5    ->for($user)

6    ->create();
```

#### [Using Magic Methods](#belongs-to-relationships-using-magic-methods)

For convenience, you may use Laravel's magic factory relationship methods to define "belongs to" relationships. For example, the following example will use convention to determine that the three posts should belong to the `user` relationship on the `Post` model:

```
1$posts = Post::factory()

2    ->count(3)

3    ->forUser([

4        'name' => 'Jessica Archer',

5    ])

6    ->create();
```

### [Many to Many Relationships](#many-to-many-relationships)

Like [has many relationships](#has-many-relationships), "many to many" relationships may be created using the `has` method:

```
1use App\Models\Role;

2use App\Models\User;

3 

4$user = User::factory()

5    ->has(Role::factory()->count(3))

6    ->create();
```

#### [Pivot Table Attributes](#pivot-table-attributes)

If you need to define attributes that should be set on the pivot / intermediate table linking the models, you may use the `hasAttached` method. This method accepts an array of pivot table attribute names and values as its second argument:

```
1use App\Models\Role;

2use App\Models\User;

3 

4$user = User::factory()

5    ->hasAttached(

6        Role::factory()->count(3),

7        ['active' => true]

8    )

9    ->create();
```

You may provide a closure-based state transformation if your state change requires access to the related model:

```
 1$user = User::factory()

 2    ->hasAttached(

 3        Role::factory()

 4            ->count(3)

 5            ->state(function (array $attributes, User $user) {

 6                return ['name' => $user->name.' Role'];

 7            }),

 8        ['active' => true]

 9    )

10    ->create();
```

You may also pass an array of pivot arrays to provide unique pivot data for each related model:

```
1$user = User::factory()

2    ->hasAttached(

3        Role::factory(),

4        [

5            ['active' => true],

6            ['active' => false],

7        ]

8    )

9    ->create();
```

If you already have model instances that you would like to be attached to the models you are creating, you may pass the model instances to the `hasAttached` method. In this example, the same three roles will be attached to all three users:

```
1$roles = Role::factory()->count(3)->create();

2 

3$users = User::factory()

4    ->count(3)

5    ->hasAttached($roles, ['active' => true])

6    ->create();
```

#### [Using Magic Methods](#many-to-many-relationships-using-magic-methods)

For convenience, you may use Laravel's magic factory relationship methods to define many to many relationships. For example, the following example will use convention to determine that the related models should be created via a `roles` relationship method on the `User` model:

```
1$user = User::factory()

2    ->hasRoles(1, [

3        'name' => 'Editor'

4    ])

5    ->create();
```

### [Polymorphic Relationships](#polymorphic-relationships)

[Polymorphic relationships](/docs/13.x/eloquent-relationships#polymorphic-relationships) may also be created using factories. Polymorphic "morph many" relationships are created in the same way as typical "has many" relationships. For example, if an `App\Models\Post` model has a `morphMany` relationship with an `App\Models\Comment` model:

```
1use App\Models\Post;

2 

3$post = Post::factory()->hasComments(3)->create();
```

#### [Morph To Relationships](#morph-to-relationships)

Magic methods may not be used to create `morphTo` relationships. Instead, the `for` method must be used directly and the name of the relationship must be explicitly provided. For example, imagine that the `Comment` model has a `commentable` method that defines a `morphTo` relationship. In this situation, we may create three comments that belong to a single post by using the `for` method directly:

```
1$comments = Comment::factory()->count(3)->for(

2    Post::factory(), 'commentable'

3)->create();
```

#### [Polymorphic Many to Many Relationships](#polymorphic-many-to-many-relationships)

Polymorphic "many to many" (`morphToMany` / `morphedByMany`) relationships may be created just like non-polymorphic "many to many" relationships:

```
1use App\Models\Tag;

2use App\Models\Video;

3 

4$video = Video::factory()

5    ->hasAttached(

6        Tag::factory()->count(3),

7        ['public' => true]

8    )

9    ->create();
```

Of course, the magic `has` method may also be used to create polymorphic "many to many" relationships:

```
1$video = Video::factory()

2    ->hasTags(3, ['public' => true])

3    ->create();
```

### [Defining Relationships Within Factories](#defining-relationships-within-factories)

To define a relationship within your model factory, you will typically assign a new factory instance to the foreign key of the relationship. This is normally done for the "inverse" relationships such as `belongsTo` and `morphTo` relationships. For example, if you would like to create a new user when creating a post, you may do the following:

```
 1use App\Models\User;

 2 

 3/**

 4 * Define the model's default state.

 5 *

 6 * @return array<string, mixed>

 7 */

 8public function definition(): array

 9{

10    return [

11        'user_id' => User::factory(),

12        'title' => fake()->title(),

13        'content' => fake()->paragraph(),

14    ];

15}
```

If the relationship's columns depend on the factory that defines it you may assign a closure to an attribute. The closure will receive the factory's evaluated attribute array:

```
 1/**

 2 * Define the model's default state.

 3 *

 4 * @return array<string, mixed>

 5 */

 6public function definition(): array

 7{

 8    return [

 9        'user_id' => User::factory(),

10        'user_type' => function (array $attributes) {

11            return User::find($attributes['user_id'])->type;

12        },

13        'title' => fake()->title(),

14        'content' => fake()->paragraph(),

15    ];

16}
```

### [Recycling an Existing Model for Relationships](#recycling-an-existing-model-for-relationships)

If you have models that share a common relationship with another model, you may use the `recycle` method to ensure a single instance of the related model is recycled for all of the relationships created by the factory.

For example, imagine you have `Airline`, `Flight`, and `Ticket` models, where the ticket belongs to an airline and a flight, and the flight also belongs to an airline. When creating tickets, you will probably want the same airline for both the ticket and the flight, so you may pass an airline instance to the `recycle` method:

```
1Ticket::factory()

2    ->recycle(Airline::factory()->create())

3    ->create();
```

You may find the `recycle` method particularly useful if you have models belonging to a common user or team.

The `recycle` method also accepts a collection of existing models. When a collection is provided to the `recycle` method, a random model from the collection will be chosen when the factory needs a model of that type:

```
1Ticket::factory()

2    ->recycle($airlines)

3    ->create();
```
