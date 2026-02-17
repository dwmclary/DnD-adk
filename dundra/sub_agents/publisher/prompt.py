PUBLISHER_PROMPT = """
**Objective:** Generate a single, complete, and visually appealing responsive HTML page for a Dungeons & Dragons mini-campaign, effectively presenting the campaign story and character information.

**Context Variables:**
* - Current Story: {{ current_story }} (String) Markdown formatted campaign story.
* - Characters Description: {{ characters_brief }} (JSON) Detailed information for each character. 
* - Generated Images: {{ generated_images }} (JSON) Object containing `characters` and `monsters` image URLs.
* - Battle Maps: {{ battle_maps }} (JSON) List of locations and their generated map URLs.
* - Monsters: {{ monsters_brief }} (JSON) List of monsters and their stat blocks.
* - Loot: {{ loot_brief }} (JSON) List of magic items and rewards.
* - Encounters & Quests: {{ encounters_and_quests }} (JSON) Random encounters and quests.

**Core Requirements:**
1.  **HTML Structure & Semantics:**
    * Generate a single, valid HTML5 document.
    * The page title (`<title>`) should be the title of the campaign, derived from `Current Story`.
    * Ensure the page is responsive to different screen sizes.
    * Image tags should reference the path "generated_images/" for images, not "generated_stories/generated_images"

2.  **Styling:**
    * Generate D&D-themed CSS. Aim for a look and feel reminiscent of classic D&D books (e.g., parchment or dark textured backgrounds, thematic borders, potentially scroll-like elements).
        * Use "Cinzel Decorative" font for main headings (h1, h2) and "EB Garamond" for body text. Ensure these fonts are imported (e.g., via Google Fonts) if not standard.
        * Implement clear visual separation between major sections (e.g., using borders, background changes, or distinct spacing).
    * Ensure proper spacing, padding, and margins for readability.

3.  **Campaign Story Section:**
    * This section should appear first under the main page heading.
    * Convert the Markdown content from `Current Story` into well-formed HTML.
    * Use appropriate heading hierarchy (e.g., `<h1>` for the main campaign title derived from `Current Story`, `<h2>` for major story sections, `<h3>` for sub-sections, etc.).
    * Format paragraphs (`<p>`) and other text elements (bold, italics) correctly.
    * For each location in the `Current Story`, add descriptive sentences for the DM to read to the party,a link to the `Battle Maps` section, and a link to the `Bestiary & Encounters` section if the location is mentioned in the `Bestiary & Encounters` section.

4.  **Battle Maps Section:**
    * Create a section titled "Key Locations & Battle Maps".
    * Display the world map of the region described in the `Current Story`.
    * For each map in `Battle Maps`:
        * Display the `location_name` as a heading.
        * Display the `description` of the location.
        * Display the map image using `image_url`.
            * Ensure the map image is large enough to be usable (e.g., full width or large modal on click).
            * Add a styled border/frame to the map image.
    * **Monsters & Encounters Section:**
    * Create a section titled "Bestiary & Encounters".
    * For each monster in `Monsters`:
        * Display the `name` and `type` prominently.
        * **Image:** Display the monster's image using the corresponding URL from `Generated Images.monsters`.
            * Look up the image by matching `monster_name` in `Generated Images.monsters` with the monster's `name`.
            * Make the image a reasonable size (e.g. 300px wide) with a scary border.
        * Create a compact stat block table or list showing `AC`, `HP`, `Speed`, `Stats` (STR/DEX/etc), `Challenge`.
        * List `Traits` and `Actions` with their descriptions.
    * **Loot & Treasures Section:**
    * Create a section titled "Treasure Hoard".
    * For each item in `Loot`:
        * Display the `name` (and `rarity`/`type`).
        * Display `description` and `mechanics`.

    * **Random Encounters Section:**
    * Create a section titled "Random Encounters".
    * For each entry in `Encounters & Quests.encounters`:
        * Create a sub-section for the `location_name`.
        * Create a HTML table or styled list representing the d8 table.
        * Columns/Fields: Roll (1-8), Type, Description, Reward.

    * **Quests & Rumors Board:**
    * Create a section titled "Quest Board".
    * For each quest in `Encounters & Quests.quests`:
        * Display as a "Quest Card" or bulletin board style entry.
        * **Title**: `quest_name`
        * **Source**: `source` (NPC or Town Board)
        * **Objective**: `objective`
        * **Rewards**: `reward_gold` and `reward_items` (highlight potions!).

5.  **Character Sections:**
    * Create a distinct section for each character detailed in `Characters Description`.
    * **Layout:** Arrange character sections in a consistent and visually appealing manner (e.g., using flexbox or grid for a gallery if multiple characters, or stacked sections).
    * **Content per Character:**
        * **Image:** Display the character's image using the corresponding URL from `Generated Images.characters`.
            * Look up the image by matching `character_name` in `Generated Images.characters` with the character's `character_name`.
            * Include descriptive `alt` text for the image (e.g., "Image of [Character Name]").
            * If an image fails to load, ensure a simple text placeholder like "[Character Name - Image Unavailable]" is visible, or a styled placeholder box.
        * **Information Structure:** Present information in a clear, organized format (e.g., using definition lists, styled divs, or sub-sections):
            * Character Name (as a prominent heading for the character's section)
            * Character Quote (if available)
            * Background and Personality
            * Features and Abilities
            * Character Stats and Attributes
            * Equipment and Actions
            * **Rumours:** (New) Display the list of rumours this NPC knows.
        * **Styling:** Apply a consistent "character sheet" feel to each character's presentation

6.  **Write the HTML:** Write the HTML file using the `Html_Writer_Tool` tool to a directory called "generated_stories" with the filename that matches the title of the story.
7.  **Be complete:** Do not skip any maps, characters, monsters, loot, encounters, or quests.  Make sure that the HTML file is complete and includes all of the information that was generated by the other agents.

**Output Format:**

* **Strictly HTML:** Return ONLY the complete HTML file content.

<Example>
 Example of a HTML template for the campaign and characters page:
    "<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>D&D Campaign & Characters</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@400;700&family=EB+Garamond:ital,wght@0,400;0,500;1,400&display=swap" rel="stylesheet">
        <style>
            /* Custom styles for D&D theme */
            body {
                font-family: 'EB Garamond', serif;
                line-height: 1.6;
                background-color: #fdf6e3; /* Parchment-like background */
                color: #3a2e25; /* Darker base text color */
            }
            h1, h2, .section-title, .stat-label, .campaign-title, .character-name-title {
                font-family: 'Cinzel Decorative', cursive;
                font-weight: 700;
            }
            .container {
                background-color: #fffaf0; /* Lighter parchment for the sheet */
                border: 1px solid #a0522d; /* Sienna border */
                box-shadow: 5px 5px 15px rgba(0,0,0,0.2);
                max-width: 56rem; /* Adjust as needed */
                margin-left: auto;
                margin-right: auto;
            }
            .stat-block {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 0.75rem;
                text-align: center;
                margin-bottom: 1rem;
            }
            .stat-item {
                border: 1px solid #deb887; /* Burlywood border */
                padding: 0.5rem;
                border-radius: 0.25rem;
                background-color: #f5f5dc; /* Beige background */
            }
            .stat-label {
                font-size: 0.8rem;
                text-transform: uppercase;
                color: #8b4513; /* SaddleBrown */
            }
            .stat-value {
                font-size: 1.125rem; /* text-lg */
                font-family: 'EB Garamond', serif;
                color: #5a3a22; /* Darker brown */
            }
            .section-title {
                text-transform: uppercase;
                margin-top: 1.5rem;
                margin-bottom: 0.75rem;
                border-bottom: 2px solid #8b4513; /* SaddleBrown border */
                padding-bottom: 0.35rem;
                color: #800000; /* Maroon color */
                font-size: 1.25rem;
            }
            .chapter-title {
                font-family: 'Cinzel Decorative', cursive;
                font-weight: 400;
                font-size: 1.1rem;
                color: #8b4513; /* SaddleBrown */
                margin-top: 1rem;
                margin-bottom: 0.25rem;
            }
            .sub-heading {
                font-weight: bold;
                margin-top: 0.75rem;
                margin-bottom: 0.25rem;
                font-family: 'EB Garamond', serif;
                font-weight: 500;
                color: #5a3a22; /* Dark brown */
            }
            .character-main-title { /* Specific style for character names */
                color: #800000; /* Maroon */
                margin-top: 1.5rem;
                font-size: 2rem; /* Slightly larger */
            }
            .quote {
                font-family: 'EB Garamond', serif;
                font-style: italic;
                color: #666;
            }
            .character-info-box {
                border: 1px solid #deb887; /* Burlywood border */
                background-color: #f5f5dc; /* Beige background */
                padding: 1rem;
                border-radius: 0.375rem;
            }
            .character-info-box hr {
                border-color: #deb887;
            }
            .character-info-box p {
                color: #5a3a22;
                margin-bottom: 0.25rem; /* Add some spacing */
            }
            /* Style for labels in the info box */
            .character-info-box .font-bold {
                color: #8b4513; /* SaddleBrown for labels */
                display: inline-block;
                min-width: 120px; /* Align labels */
                font-weight: bold; /* Ensure boldness */
                padding-right: 0.5em; /* Space after label */
            }
            .separator-hr {
                border-top-width: 2px;
                border-color: #8b4513; /* SaddleBrown */
                margin-top: 2rem;
                margin-bottom: 2rem;
            }
            /* Ensure consistent label color (overrides Tailwind if needed) */
            .font-bold.text-amber-900 {
                color: #8b4513 !important; /* SaddleBrown */
            }
            .character-sheet {
                border: 1px dashed #a0522d; /* Add subtle border around each character */
                padding: 1.5rem;
                margin-bottom: 2rem;
                border-radius: 0.5rem;
                background-color: #fffef7; /* Slightly different bg for character area */
            }
            .prose p { margin-bottom: 0.75em; } /* Spacing for campaign text */

            /* Ensure KaTeX renders correctly */
            .katex { font-size: 1.1em !important; }

            /* Responsive adjustments */
            @media (max-width: 768px) {
                .stat-block {
                    grid-template-columns: repeat(2, 1fr);
                }
                .main-content {
                    flex-direction: column;
                }
                .left-column, .right-column {
                    width: 100%;
                }
                .character-image-container {
                    margin-left: auto;
                    margin-right: auto;
                    max-width: 200px; /* Adjust image width */
                }
                h1 { font-size: 1.75rem; }
                .section-title { font-size: 1.1rem; }
                .character-main-title { font-size: 1.6rem; }
                .character-info-box .font-bold { min-width: 100px; } /* Adjust label width */
            }
        </style>
    </head>
    <body class="p-4 md:p-8">
        <div class="container mx-auto p-6 md:p-8 rounded-lg">

            <div class="mb-8 text-stone-800">
                <h2 class="section-title text-center">Campaign Story</h2>
                <div class="mt-4 prose prose-lg prose-stone max-w-none">
                    <p>The land of Aeridor is shrouded in an unnatural twilight. Ancient forests groan under the weight of corruption,</p>
    <p>and once-bustling cities huddle behind fortified walls, fearing the shadows that creep from the blighted lands.</p>
    <p>Whispers speak of the Serpent&#x27;s Eye, a malevolent artifact sought by a shadowy cult known as the Ophidian Coil.</p>
    <p>It is said this artifact grants immense power over life and death, and the Coil intends to use it to plunge Aeridor into eternal darkness.</p>
    <p>Our heroes, drawn together by fate or perhaps misfortune, find themselves entangled in this growing conflict.</p>
    <p>From humble beginnings in threatened villages to navigating the treacherous politics of besieged kingdoms,</p>
    <p>they must unravel the Coil&#x27;s plans, confront monstrous beasts twisted by dark magic, and ultimately decide the fate of Aeridor.</p>
                </div>
            </div>
            <hr class="separator-hr">
            <h2 class="section-title text-center mb-8">Player Characters</h2>

            <div class="character-sheet mb-12">
                <div class="text-center mb-6">
                    <h1 class="character-main-title uppercase">Torvin Stonebeard</h1>
                    <p class="quote mt-2">"&quot;By Moradin&#x27;s beard, stand behind me! I&#x27;ll shield ye!&quot;"</p>
                </div>

                <div class="flex flex-col md:flex-row gap-8 main-content">
                    <div class="md:w-1/2 left-column text-stone-800">
                        <h2 class="section-title">Background & Personality</h2>
                        <p class="mb-4"><p>Torvin is a sturdy and devout dwarf, dedicated to healing and protecting others. Gruff but kind-hearted, he follows the tenets of Moradin, seeking to mend the broken and stand firm against evil.</p></p>
                        <h3 class='sub-heading'>Background: Acolyte</h3><p>No specific details provided.</p>
                        <p><span class="font-bold text-amber-900">Bond:</span> Feels responsible for the well-being of his companions.</p>
                        <p><span class="font-bold text-amber-900">Flaw:</span> Stubborn and slow to change his mind once it&#x27;s set.</p>
                        <h2 class="section-title">Features & Abilities</h2><p>Spellcasting, Disciple of Life, Channel Divinity (Preserve Life)</p>
                    </div>

                    <div class="md:w-1/2 right-column">
                        <div class="mb-6 text-center character-image-container">
                            <img src="https://placehold.co/250x250/b8860b/4d3a1f?text=Torvin" alt="Torvin Stonebeard Portrait"
                                class="rounded-lg shadow-md inline-block border-2 border-amber-800"
                                onerror="this.onerror=null; this.src='https://placehold.co/200x200/f5f5dc/8b4513?text=Image+Missing'; this.alt='Image missing';">
                        </div>
                        <div class="p-4 rounded-md mb-6 character-info-box">
                            <p class="text-center text-sm">Hill Dwarf, Cleric (Life Domain) 1, Lawful Good</p>
                            <hr class="my-2">
                            <p><span class="font-bold">Armor Class:</span> 18 (Scale Mail, Shield)</p>
                            <p><span class="font-bold">Hit Points:</span> 10 (1d8 + 2)</p>
                            <p><span class="font-bold">Speed:</span> 25 ft.</p>
                            <hr class="my-2">
                            <div class="stat-block my-4"><div class="stat-item"><div class="stat-label">STR</div><div class="stat-value">14 (+2)</div></div><div class="stat-item"><div class="stat-label">DEX</div><div class="stat-value">10 (+0)</div></div><div class="stat-item"><div class="stat-label">CON</div><div class="stat-value">15 (+2)</div></div><div class="stat-item"><div class="stat-label">INT</div><div class="stat-value">8 (-1)</div></div><div class="stat-item"><div class="stat-label">WIS</div><div class="stat-value">16 (+3)</div></div><div class="stat-item"><div class="stat-label">CHA</div><div class="stat-value">12 (+1)</div></div></div>
                            <hr class="my-2">
                            <p><span class="font-bold">Proficiency Bonus:</span> +2</p>
                            <p><span class="font-bold">Saving Throws:</span> Wis +5, Cha +3</p>
                            <p><span class="font-bold">Skills:</span> Medicine +5, Religion +3, Insight +5</p>
                            <p><span class="font-bold">Languages:</span> Common, Dwarvish</p>
                            <p><span class="font-bold">Tool Prof:</span> Smith&#x27;s tools, Brewer&#x27;s supplies</p>
                            <p><span class="font-bold">Armor Prof:</span> Light and medium armor, shields</p>
                            <p><span class="font-bold">Weapon Prof:</span> Simple weapons</p>
                        </div>
                        <div class="text-stone-800">
                            <h2 class="section-title">Actions</h2><p>Warhammer Attack: +4 to hit, 1d8+2 bludgeoning. Sacred Flame cantrip. Cure Wounds spell.</p>
                            <h2 class="section-title">Equipment</h2>
                            <p><p>Scale mail, Shield, Warhammer, Holy symbol (Anvil of Moradin), Healing potions (x2), Healer&#x27;s kit, 10 gp.</p></p>
                        </div>
                    </div>
                </div>
            </div>
            <hr class="separator-hr">

            <div class="character-sheet mb-12">
                <div class="text-center mb-6">
                    <h1 class="character-main-title uppercase">Willow Greenleaf</h1>
                    <p class="quote mt-2">"&quot;The wind carries whispers... let&#x27;s listen.&quot;"</p>
                </div>

                <div class="flex flex-col md:flex-row gap-8 main-content">
                    <div class="md:w-1/2 left-column text-stone-800">
                        <h2 class="section-title">Background & Personality</h2>
                        <p class="mb-4"><p>Willow is quiet and observant, more comfortable in the wilds than in cities. She is a skilled tracker and archer, fiercely protective of the natural world and those few she calls friends.</p></p>
                        <h3 class='sub-heading'>Background: Outlander</h3><p>No specific details provided.</p>
                        <p><span class="font-bold text-amber-900">Bond:</span> Protects an ancient grove deep within the Whisperwood.</p>
                        <p><span class="font-bold text-amber-900">Flaw:</span> Deeply distrustful of arcane magic users.</p>
                        <h2 class="section-title">Features & Abilities</h2><p>Favored Enemy (Goblinoids), Natural Explorer (Forest), Fighting Style (Archery)</p>
                    </div>

                    <div class="md:w-1/2 right-column">
                        <div class="mb-6 text-center character-image-container">
                            <img src="https://oaidalleapiprodscus.blob.core.windows.net/private/org-pm2YROQzuJ8CAtKXQBiLlKcQ/user-ltxpTeyboXGDJyM2JY2McOB5/img-CeFGcZRyQGxr4JvjA2NWyFfe.png?st=2025-05-06T00%3A12%3A42Z&amp;se=2025-05-06T02%3A12%3A42Z&amp;sp=r&amp;sv=2024-08-04&amp;sr=b&amp;rscd=inline&amp;rsct=image/png&amp;skoid=cc612491-d948-4d2e-9821-2683df3719f5&amp;sktid=a48cca56-e6da-484e-a814-9c849652bcb3&amp;skt=2025-05-06T00%3A10%3A24Z&amp;ske=2025-05-07T00%3A10%3A24Z&amp;sks=b&amp;skv=2024-08-04&amp;sig=84IAlVCFykU1fWkDmvH27B8d6YHBAl0NeTwNF/QFgrQ%3D" alt="Willow Greenleaf Portrait"
                                class="rounded-lg shadow-md inline-block border-2 border-amber-800"
                                onerror="this.onerror=null; this.src='https://placehold.co/200x200/f5f5dc/8b4513?text=Image+Missing'; this.alt='Image missing';">
                        </div>
                        <div class="p-4 rounded-md mb-6 character-info-box">
                            <p class="text-center text-sm">Wood Elf, Ranger (Hunter Conclave) 1, Neutral Good</p>
                            <hr class="my-2">
                            <p><span class="font-bold">Armor Class:</span> 15 (Leather Armor)</p>
                            <p><span class="font-bold">Hit Points:</span> 11 (1d10 + 1)</p>
                            <p><span class="font-bold">Speed:</span> 35 ft.</p>
                            <hr class="my-2">
                            <div class="stat-block my-4"><div class="stat-item"><div class="stat-label">STR</div><div class="stat-value">12 (+1)</div></div><div class="stat-item"><div class="stat-label">DEX</div><div class="stat-value">17 (+3)</div></div><div class="stat-item"><div class="stat-label">CON</div><div class="stat-value">13 (+1)</div></div><div class="stat-item"><div class="stat-label">INT</div><div class="stat-value">11 (+0)</div></div><div class="stat-item"><div class="stat-label">WIS</div><div class="stat-value">15 (+2)</div></div><div class="stat-item"><div class="stat-label">CHA</div><div class="stat-value">9 (-1)</div></div></div>
                            <hr class="my-2">
                            <p><span class="font-bold">Proficiency Bonus:</span> +2</p>
                            <p><span class="font-bold">Saving Throws:</span> Str +3, Dex +5</p>
                            <p><span class="font-bold">Skills:</span> Stealth +5, Survival +4, Perception +4, Athletics +3</p>
                            <p><span class="font-bold">Languages:</span> Common, Elvish, Sylvan</p>
                            
                            <p><span class="font-bold">Armor Prof:</span> Light and medium armor, shields</p>
                            <p><span class="font-bold">Weapon Prof:</span> Simple and martial weapons</p>
                        </div>
                        <div class="text-stone-800">
                            <h2 class="section-title">Actions</h2><p>Longbow Attack: +7 to hit, 1d8+3 piercing. Shortsword Attack: +5 to hit, 1d6+3 piercing.</p>
                            <h2 class="section-title">Equipment</h2>
                            <p><p>Leather armor, Longbow, 20 arrows, Two shortswords, Explorer&#x27;s pack, Animal companion (Wolf named Shadow), 15 gp.</p></p>
                        </div>
                    </div>
                </div>
            </div>
            <hr class="separator-hr">

            <div class="character-sheet mb-12">
                <div class="text-center mb-6">
                    <h1 class="character-main-title uppercase">Zephyr Quickfoot</h1>
                    <p class="quote mt-2">"&quot;A little song, a little dance, and even a dragon might reconsider!&quot;"</p>
                </div>

                <div class="flex flex-col md:flex-row gap-8 main-content">
                    <div class="md:w-1/2 left-column text-stone-800">
                        <h2 class="section-title">Background & Personality</h2>
                        <p class="mb-4"><p>Zephyr is charming, witty, and perpetually optimistic, even in dire situations. He uses his music and quick thinking to navigate trouble, preferring diplomacy or trickery over direct confrontation. Loves a good story and a cheering crowd.</p></p>
                        <h3 class='sub-heading'>Background: Entertainer</h3><p>No specific details provided.</p>
                        <p><span class="font-bold text-amber-900">Bond:</span> Seeks fame and recognition across the land.</p>
                        <p><span class="font-bold text-amber-900">Flaw:</span> Sometimes exaggerates stories to the point of outright lies.</p>
                        <h2 class="section-title">Features & Abilities</h2><p>Spellcasting, Bardic Inspiration (d6)</p>
                    </div>

                    <div class="md:w-1/2 right-column">
                        <div class="mb-6 text-center character-image-container">
                            <img src="https://placehold.co/250x250/87ceeb/3a5fcd?text=Zephyr" alt="Zephyr Quickfoot Portrait"
                                class="rounded-lg shadow-md inline-block border-2 border-amber-800"
                                onerror="this.onerror=null; this.src='https://placehold.co/200x200/f5f5dc/8b4513?text=Image+Missing'; this.alt='Image missing';">
                        </div>
                        <div class="p-4 rounded-md mb-6 character-info-box">
                            <p class="text-center text-sm">Lightfoot Halfling, Bard (College of Lore) 1, Chaotic Good</p>
                            <hr class="my-2">
                            <p><span class="font-bold">Armor Class:</span> 13 (Leather Armor)</p>
                            <p><span class="font-bold">Hit Points:</span> 9 (1d8 + 1)</p>
                            <p><span class="font-bold">Speed:</span> 25 ft.</p>
                            <hr class="my-2">
                            <div class="stat-block my-4"><div class="stat-item"><div class="stat-label">STR</div><div class="stat-value">8 (-1)</div></div><div class="stat-item"><div class="stat-label">DEX</div><div class="stat-value">15 (+2)</div></div><div class="stat-item"><div class="stat-label">CON</div><div class="stat-value">12 (+1)</div></div><div class="stat-item"><div class="stat-label">INT</div><div class="stat-value">13 (+1)</div></div><div class="stat-item"><div class="stat-label">WIS</div><div class="stat-value">10 (+0)</div></div><div class="stat-item"><div class="stat-label">CHA</div><div class="stat-value">16 (+3)</div></div></div>
                            <hr class="my-2">
                            <p><span class="font-bold">Proficiency Bonus:</span> +2</p>
                            <p><span class="font-bold">Saving Throws:</span> Dex +4, Cha +5</p>
                            <p><span class="font-bold">Skills:</span> Acrobatics +4, Performance +5, Persuasion +5, Deception +5, Sleight of Hand +4</p>
                            <p><span class="font-bold">Languages:</span> Common, Halfling, Elvish</p>
                            <p><span class="font-bold">Tool Prof:</span> Lute, Flute, Thieves&#x27; tools</p>
                            <p><span class="font-bold">Armor Prof:</span> Light armor</p>
                            <p><span class="font-bold">Weapon Prof:</span> Simple weapons, hand crossbows, longswords, rapiers, shortswords</p>
                        </div>
                        <div class="text-stone-800">
                            <h2 class="section-title">Actions</h2><p>Rapier Attack: +4 to hit, 1d8+2 piercing. Vicious Mockery cantrip. Dissonant Whispers spell.</p>
                            <h2 class="section-title">Equipment</h2>
                            <p><p>Leather armor, Rapier, Lute, Diplomat&#x27;s pack, Disguise kit, Thieves&#x27; tools, 20 gp.</p></p>
                        </div>
                    </div>
                </div>
            </div>
            <hr class="separator-hr">
        </div> 
    </body>
    </html>"
</Example>

"""
