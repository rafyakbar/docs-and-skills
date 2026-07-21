---
name: laravel-migration-development
description: "Activate when creating or updating Laravel database migrations in this project. Covers table creation, schema modification, indexes, foreign keys, and migration organization. First checks if the project uses nscreed/laravel-migration-paths for subfolder support; otherwise defaults to flat database/migrations/. Always activate when the user asks to create a migration, add a table, modify schema, or add indexes. Do NOT activate for non-Laravel projects or seeding."
license: MIT
metadata:
  author: Rafy
---

# Laravel Migration Development

## When to Apply

- Creating a new migration for tables, columns, indexes, or foreign keys
- Updating existing schema (adding, modifying, dropping columns)
- Adding or modifying indexes and foreign key constraints
- Modifying or dropping existing database objects through migrations

## Overview

Laravel migrations are version-controlled schema definitions. Before creating any migration, check whether the project uses subfolder organization.

### Check for Subfolder Support

Look in `composer.json` for `nscreed/laravel-migration-paths`:

```powershell
composer show nscreed/laravel-migration-paths
```

If present, migrations can be organized into subfolders. If absent, all migrations go flat into `database/migrations/`.

#### With `nscreed/laravel-migration-paths`

```
database/migrations/
├── tables/       → Tables, indexes, foreign keys, constraints
└── views/        → Database views
```

#### Without (default Laravel)

```
database/migrations/   ← All migrations flat here
```

### Migration File Naming

`[YEAR]_[MONTH]_[DAY]_[HOUR][MINUTE][SECOND]_[action]_[name].php`

Timestamp format: `Y_m_d_His` (e.g., `2026_05_08_104550`).

## Step-by-Step

### Step 1: Get the Current Timestamp

```powershell
php artisan tinker --execute "echo now()->format('Y_m_d_His');"
```

```php
$timestamp = now()->format('Y_m_d_His');
```

### Step 2: Choose the Directory and Name

Check for `nscreed/laravel-migration-paths` first.

#### With subfolder support

| Type | Directory | Example Filename |
|------|-----------|------------------|
| Table | `database/migrations/tables/` | `2026_05_08_104550_create_invoices_table.php` |
| View | `database/migrations/views/` | `2026_05_08_104550_create_invoice_summary_view.php` |

#### Without subfolder support

All migrations go in `database/migrations/` with a descriptive name:

```
database/migrations/2026_05_08_104550_create_invoices_table.php
```

### Step 3: Write the Migration

#### Creating a New Table

Use `Schema::create()` with `Blueprint`:

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('products', function (Blueprint $table) {
            $table->id();
            $table->string('kode', 50)->unique();
            $table->string('nama', 200)->index();
            $table->text('description')->nullable();
            $table->integer('urutan')->default(0);
            $table->boolean('is_active')->default(true);
            $table->foreignId('category_id')
                ->constrained('categories')
                ->cascadeOnUpdate()
                ->restrictOnDelete();
            $table->timestamps();
            $table->softDeletes()->index();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('products');
    }
};
```

#### Common Column Types

| Type | Blueprint Method |
|------|-----------------|
| Big auto-increment | `$table->id()` |
| UUID primary | `$table->uuid('id')->primary()` |
| String (VARCHAR) | `$table->string('col', length)` |
| Text (longtext) | `$table->text('col')` |
| Integer | `$table->integer('col')` |
| BigInteger | `$table->bigInteger('col')` |
| Unsigned integer | `$table->unsignedInteger('col')` |
| Decimal | `$table->decimal('col', 18, 2)` |
| Float | `$table->float('col', 8, 2)` |
| Boolean | `$table->boolean('col')` |
| Date | `$table->date('col')` |
| DateTime | `$table->dateTime('col')` |
| Timestamp | `$table->timestamp('col')` |
| JSON | `$table->json('col')` or `$table->jsonb('col')` |
| Enum | `$table->string('col')->index()` (prefer string + index over DB enum) |
| Foreign key | `$table->foreignId('col')` |
| Timestamps | `$table->timestamps()` |
| Soft deletes | `$table->softDeletes()->index()` |

#### Common Column Modifiers

| Modifier | Usage |
|----------|-------|
| `->nullable()` | Allow NULL values |
| `->default(value)` | Set default value |
| `->unsigned()` | Unsigned for integers |
| `->unique()` | Add unique constraint |
| `->index()` | Add index |
| `->after('col')` | Position after column (MySQL) |
| `->first()` | Position first (MySQL) |
| `->comment('text')` | Add column comment |
| `->charset('utf8mb4')` | Set charset |
| `->collation('utf8mb4_unicode_ci')` | Set collation |

#### Common Table Patterns (ordered by position)

| # | Pattern | Code |
|---|---------|------|
| 1 | Primary key | `$table->id();` |
| 2 | UUID | `$table->uuid('id')->primary();` |
| 3 | Timestamps | `$table->timestamps();` |
| 4 | Soft deletes | `$table->softDeletes()->index();` |
| 5 | Sequence / sort order | `$table->integer('urutan')->default(0);` |
| 6 | Standard foreign key | `$table->foreignId('xxx_id')->constrained('table')->cascadeOnUpdate()->restrictOnDelete();` |
| 7 | Nullable foreign key | `$table->foreignId('yyy_id')->nullable()->constrained('table')->cascadeOnUpdate()->nullOnDelete();` |
| 8 | Index | `$table->string('kode')->index();` |
| 9 | Unique | `$table->unique(['col_a', 'col_b'], 'index_name');` |
| 10 | Composite index | `$table->index(['col_a', 'col_b'], 'index_name');` |
| 11 | Default | `$table->boolean('is_active')->default(true);` |
| 12 | Nullable | `$table->text('notes')->nullable();` |
| 13 | Decimal amount | `$table->decimal('amount', 18, 2)->default(0);` |

#### Modifying Existing Tables

```php
Schema::table('products', function (Blueprint $table) {
    // Add columns
    $table->string('new_column', 100)->after('nama');
    $table->text('notes')->nullable()->after('description');

    // Modify columns
    $table->string('nama', 255)->change();
    $table->string('kode', 100)->nullable()->change();

    // Rename columns
    $table->renameColumn('old_name', 'new_name');

    // Drop columns
    $table->dropColumn(['col1', 'col2']);

    // Indexes
    $table->index('new_column');
    $table->unique(['col_a', 'col_b'], 'unique_pair');
    $table->fullText('description');
    $table->dropIndex(['some_index']);
    $table->dropUnique(['unique_pair']);
    $table->renameIndex('old_index', 'new_index');

    // Foreign keys
    $table->foreignId('user_id')->constrained()->cascadeOnDelete();
    $table->dropForeign(['user_id']);
});
```

> **Note:** `->change()` requires the `doctrine/dbal` or `laminas/laminas-diactoros` package. Column modifications are database-specific and may not work on all platforms.

#### Views

Only if subfolder support exists (with `nscreed/laravel-migration-paths`):

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Support\Facades\DB;

return new class extends Migration
{
    public function up(): void
    {
        DB::statement("
            create or replace view active_users as
            select id, name, email from users where active = true
        ");
    }

    public function down(): void
    {
        DB::statement('drop view if exists active_users');
    }
};
```

### Step 4: Register (if applicable)

If the project uses `nscreed/laravel-migration-paths`, no registration is needed. If it uses a custom service provider or manual migration path registration, register the path in `AppServiceProvider`:

```php
// App\Providers\AppServiceProvider
public function boot(): void
{
    Migration::paths([
        database_path('migrations/tables'),
        database_path('migrations/views'),
    ]);
}
```

## Important Rules

- **NEVER run `php artisan migrate`.** Only create/edit the migration file.
- Always define both `up()` and `down()` methods. `down()` must cleanly reverse `up()`.
- Use `Schema::create()` for new tables, `Schema::table()` for alterations.

## Common Pitfalls

- **Wrong timestamp** — Use `Y_m_d_His`. Always fetch `now()->format('Y_m_d_His')` first.
- **Assuming subfolders exist** — Default Laravel does not support subfolders. Check for `nscreed/laravel-migration-paths` first.
- **Missing indexes** — Searchable columns (`string`, `text`) should have `->index()`.
- **Soft deletes without index** — Always chain `->index()` on `$table->softDeletes()`.
- **Incomplete `down()`** — Drop columns in reverse order, drop foreign keys before columns, drop tables.
- **Forgetting `nullable()`** — Columns that allow NULL must have `->nullable()`.
- **No default for non-nullable columns** — Non-nullable columns need `->default()` unless required.
- **Using DB enum** — Prefer `string` + `index` + validation over DB enum types for portability.
- **`->change()` without doctrine/dbal** — Requires `doctrine/dbal` or `laminas/laminas-diactoros`.
- **Forgetting `->constrained()`** — `foreignId('xxx_id')` alone does not create a constraint; chain `->constrained('table')`.

## Checklist

### Structure
- [ ] Timestamp obtained via `now()->format('Y_m_d_His')`
- [ ] File placed in correct directory (check for `nscreed/laravel-migration-paths` first)
- [ ] Filename follows pattern `Y_m_d_His_action_name.php`

### Content
- [ ] `up()` and `down()` methods both defined
- [ ] `down()` cleanly reverses `up()`
- [ ] Searchable columns have `->index()`
- [ ] `softDeletes()` chained with `->index()`
- [ ] Foreign keys use `cascadeOnUpdate()` and `restrictOnDelete()` (or `nullOnDelete()` if nullable)
- [ ] `->nullable()` on columns that allow NULL
- [ ] `->default()` on non-nullable columns
- [ ] Sequence/sort column (`urutan`) added where ordering is needed
- [ ] No composite unique without checking for duplicates first

### Validation
- [ ] Confirm no naming conflict with existing migrations
- [ ] Migration file does not contain `php artisan migrate` command
