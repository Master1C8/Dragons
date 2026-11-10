# Ukrainian special-scene wording

Authoring input is [translation.json](translation.json). The first
batch covered 46 of 1,947 package IDs in five of the 27 current
special-scene groups. It follows the common stage and review protocol
in [HANDOFF.md](../../HANDOFF.md). The current state follows the
batch and evidence history below.

| Input | Identity |
| --- | --- |
| Shared v42 inventory | `79a38356e74a513bba512f2a23f462d4a6a25bf069519bab03aef96be24f476d` |
| Paired Yarn scope | `753f54cf058bee240e56ab6ddf67b3c549f6804853e493239de097cebef65b30` |
| SiteForMods English glossary | `29b0bb56`, canonical fingerprint `3d261921e114b6feab10f57ad54d43674a75e991d94937686155b92cce399dc3` |
| SiteForMods Ukrainian ordered locale map | `4ff95ddd932acd5f990c8f8f11f76ecf372976200645872adc464a5b4842b4a0` |
| First authored batch | `c7c088e13254489bc23e4ad64a2c84361e320f8f0a1383c39291b82009fa210e` |

The author checked the Ukrainian wording against the paired English
source, the indexed choice groups and the glossary. The editor and
runtime columns below concern this batch only.

| Case | Wording decision and acceptance controls | State |
| --- | --- | --- |
| `anonymous-dragon-address` (20 IDs) | Keep both the unnamed dragon and player gender-neutral. The dragon asks about remaining dirt, and the player can apologize or explain unfamiliarity with the button. Retain the sound «БРРТ», silence option and «Так!» versus «ТАК!». Exercise both branches in all four groups and reject any choice-order change, added identity or shift in who acts. The source buzzing finish-command limitation remains as documented in the [source registry](../evidence/generic-dragon-entries-20261110.md). | Author checked. Ukrainian scene runs and visual review pending. |
| `big-c-nickname` (14 IDs) | Conrad calls himself «Великий К», tying the joke to Конрад. One reply echoes the nickname and he drops it. The other uses «Конраде». Retain both destinations, the Ryan relationship reference and the italic spans. Reject loss of the initial or inversion of the two replies. | Author checked. Both Ukrainian branches and visual review pending. |
| `alexander-proletarian-register` (7 IDs) | Keep «пролетарська» as the high-register descriptor, «проле-» as the false start and «робітничому класу» as the clarification. The alternative thanks him and leads to the public-access comment. The English spelling error in the Windows source does not affect the wording. Preserve the original tags and test each destination and convergence. | Author checked. Both Ukrainian branches and visual review pending. |
| `new-slot-display` (4 package IDs) | Use «НОВИЙ» for the runtime slot label and «Новий» for the three serialized labels. Both describe a new save slot. Exercise all three empty slots and reject changed progress formats or a change to an occupied slot's state. | Author checked. Empty-slot runtime result recorded below. Occupied-slot and visual checks pending. |
| `missing-yarn-line-display` (1 package ID) | Use «!! ПОМИЛКА: Репліку не знайдено!» for the existing error route. A missing line must still reach the fallback and a valid line must not. | Author checked. Managed bytes verified. Ukrainian runtime error control pending. |

Both complete builders passed a private structure control containing
the 46 authored values and original English for all remaining IDs.
Read-back matched the 41 authored Yarn values and all other Yarn
strings, key order and metadata. The two managed strings were present
in the built assemblies. The stock font contains all 58 display code
points in this batch. English control values stay outside the authoring
file and do not count as translated or reviewed.

The paired background New Game test saw three active «НОВИЙ» and
three active «Новий» labels on both builds. The initial observers
still expected the Russian spelling for the serialized labels.
The successful repeat changed that expectation alone. The macOS
and CrossOver observers recorded no foreground windows, and the
original profiles matched their pre-run hashes.

Local control assets and receipts are under
`localization/work/uk-special-scenes-20261110.pE2LiD/`.

## Second batch

The draft now has 136 authored IDs, 90 of them new. All 46 earlier
values are exact. The draft SHA-256 is
`619bbc115a5ec23e3575dff9ff62cc1397e99ed1a6e3d5f5488ed4cf0285dcfc`.
The source inventory, Yarn scope and glossary bindings above still apply.

| Case | Ukrainian decision and remaining acceptance check |
| --- | --- |
| `alexander-number-seven-taste` | Keep the numeral 7 and «жовтий лайм». The lemon guess must still lead to a correction, the disbelief to the repeated rebuttal, and deference to the appeal-to-authority joke. |
| `alexander-family-crest` | Introduce the object as an unfamiliar emblem, then identify it as «родова емблема». Retain all seven shrinking spans and the four-nations joke in the smallest region. Verify the two responses and the region boundaries at runtime. |
| `alexander-college-self-introduction` | Use «Громадський коледж тауматургії Бернсвіка» and «Александер». Keep the formal self-praise and trailing colon in the separate speaker display field. Verify the display and both question responses, with the preceding secrecy lines as context. |
| `alexander-teacher-professor-correction` | Distinguish «дракона-вчителя» from the interrupted «Професора». The other reply opens the gate without setting up the correction. Verify both continuations. |
| `dirty-double-meaning` | Keep the two readings of «брудний» and the original italic and tilde emphasis. Preserve each explicit outcome and the distinct price response. Verify both branch paths and that the staged vowels shrink in order. |
| `professional-double-meaning` | The player says «Я роблю це професійно» without a gendered self-title. Conrad echoes the claim and switches who receives the service. Preserve the live choice IDs and the different response paths. |
| `conrad-special-endings` | Use the glossary euphemism «особливі завершення» and preserve the escalation from the literal reading to the blunt clarification. Keep the refusal, assent and uncertainty choices distinct. The two differing English strings share Ukrainian wording because the difference is punctuation. |
| `conrad-emphatic-greetings`, `conrad-scales-aside` | Use «АГОВ» for both greetings. Restrict the gradient to the shout and preserve the small, italic aside about the scales. Check the size reset and the exact end of each styled span. |
| `ryan-branch-hesitation-sizing` | Keep the repeated acknowledgement and disfluency as the response shrinks, with each phrase in its corresponding original size region. Verify the original option target and all size transitions. |

The author checked these ten groups against the paired English source
and their indexed dependencies. Ukrainian branch runs, pixel review
and independent editorial review remain pending for the new groups.
Both complete builders passed a diagnostic control with the authored
values and English for the untouched IDs. Read-back verified all 130
authored Yarn values, the new managed Alexander display string, the
previous managed strings, and exact preservation of all other Yarn
text, IDs and metadata. The original font covers all 69 display
code points in the draft. Diagnostic assets and receipts are under
`localization/work/uk-special-scenes-2-20261110.VCXXS1/`.

## Third batch

The draft now has 256 authored IDs, with 120 new values and all 136
earlier values unchanged. It covers the wording of all 27 registered
cases. The draft SHA-256 is
`a2f41a55b50fadd892b9017490b0b086c19b291ba3b0534f60766792f4229706`.
The source inventory, Yarn scope and glossary bindings above still apply.

| Case | Ukrainian decision and remaining acceptance check |
| --- | --- |
| `yarn-missing-named-destinations` | Translate eight visible suffix lines shared with the restored destinations. Keep the 15 marker values exact. Exercise all five destinations in ordinary play and confirm the visible continuation and subsequent state. |
| `yarn-alexander-question-once-state` | Keep the formal address and seven distinct prompts, two of which were already authored. Verify consumed choices stay consumed while the remaining choices stay selectable. |
| `alexander-romance-route` | Distinguish acceptance from the polite decline. Preserve the gold label and smaller route note. Verify both destinations and the resulting romance state. |
| `ryan-conrad-romance-routing` | Separate the options that open a route from the choices that commit it. Preserve who is introduced to whom, the two size regions in Ryan's hesitant option, and the three different outcomes. Verify state and option fit. |
| `editor-route-prompt` | Keep the prompt and its two short replies distinct from the player's dialogue. Verify it stays limited to the editor and leaves ordinary play unaffected. |
| `mouth-full-speech` | Use «Кофик», «гофорити» and «Дякуф» for Ryan's muffled speech. Keep the gate request and the two replies recognizable. Verify both paths and the recovery of clear speech. |
| `salmon-guy-dragon` | Keep the self-correction from «хлопців» to «дракон» and the distinction between accepting seafood and suggesting another venue. Preserve the shared date-choice IDs. |
| `movie-title-choices` | Keep three distinct titles and the numeral 2. Use «Йіп-Мен — Останній Йіп» with an em dash because Yarn reads the first colon as a speaker separator. Verify the reactions and the final convergence. |
| `conrad-height-euphemism` | Use «з обмеженнями у вертикальному вимірі» in both sequences. Retain the contrast with «маленький» and keep the prospective date unnamed in the relevant reply. Verify both introductions and reactions. |
| `ryan-question-about-a-question` | Preserve the playful opening, the turn toward a difficult relationship and the distinct supportive replies. Keep Ryan's italic emphasis and verify the branches converge at the intended point. |
| `kobold-yip-speech` | Use «Йіп» for the utterance and keep its parenthetical gloss in the original smaller region. Check both the long gloss and the abrupt short one for fit. |
| `kobold-yip-film-title` | Reuse both authored IDs from the film choices. Check the shared title and spoken «Йіп» remain consistent in their two contexts. |

Both complete builders passed a control with English for the untouched
IDs. Read-back from each package matched all 250 authored Yarn values,
the remaining original Yarn values, metadata and key order. Each
packaged Yarn program matched its pinned repaired fingerprint and
contained all five destinations. Managed display strings, the macOS
signature and Windows ZIP integrity also passed. Both packaged source
fonts cover all 75 display code points used by the draft. Branch runs,
rendered fit and independent editorial review are still pending for
these additions. Diagnostic packages and receipts are under
`localization/work/uk-special-scenes-3-20261110.bnGbL5/`.

## Fourth batch

The draft now has 407 authored IDs. The additional 151 are the
missing responses and follow-ups of five registered cases. All 256
earlier values are exact. The draft SHA-256 is
`f8f6acab47668fbcd8bebaa953dedcfeb35b628646fd82c13a40deb6e0d6d8db`.
The pinned source, scope and glossary bindings above are unchanged.

| Case | New IDs | Context covered |
| --- | ---: | --- |
| `alexander-college-self-introduction` | 2 | The warning about another policy violation and the request to keep the incident from the college. |
| `alexander-teacher-professor-correction` | 13 | The greeting, crest recognition, alchemy lesson, conflicting readings of how dirty Alexander is, and gate request. |
| `alexander-romance-route` | 15 | The question about his attractiveness, the invitation to the college library, and the separate responses to acceptance and decline. |
| `ryan-conrad-romance-routing` | 69 | The suggestion and invitation exchanges, the three route outcomes and their distinct farewells. |
| `yarn-alexander-question-once-state` | 52 | The exit option and follow-ups to the seven questions, including the double sense of looking up to Alexander. |

The case boundary uses the source IDs established in the previous
route tests and the pinned worklist for the English wording. Only
two additions have different English strings across platforms.
Both differences are punctuation or spelling. Each uses one explicit
shared Ukrainian value.

Both normal builders passed the diagnostic control. Read-back
matched the 401 authored Yarn table values, the separate managed
display values and the untouched Yarn table data. Each packaged font
contains all 76 display code points in the current draft. The macOS
app passed strict signature verification and the Windows ZIP passed
its integrity check.

| Packaged program replay | Scenarios per platform | Unique Yarn IDs checked per platform |
| --- | ---: | ---: |
| Alexander's question state and nested responses | 6 | 60 |
| Alexander's college introduction | 2 | 11 |
| Romance routes, including the existing-flag decline control | 9 | 106 |
| Restored transitions and final commands | 5 | 8 |

The two packaged Yarn programs produced the same routes, choices,
flag outcomes and commands in desktop .NET. The separate table
read-back matched the authored text for every ID emitted or offered
in these traces. For `line:4b36ea4e` it verified the exact English
table value and the Ukrainian text in the managed display adapter.
The restored Conrad beat-up destination issues its commands without
a visible line. The replay sets starting variables and replaces
Unity's presenters and command handlers with callbacks. Actual Unity
progression, pixel fit and independent editorial review for the new
wording remain pending.

Control packages, replay sources and receipts are under
`localization/work/uk-special-scene-closure-20261110.sbqndo/`.
The SHA-256 of `route-table-readback.log` is
`74405387032afc498febd81512083c10e6aee7f6866552276493177c2c2b5844`.

## Alexander display in Unity

The isolated macOS player and Windows player through CrossOver both
used the fourth-batch package with two RunLine operands redirected
in the test copy of `Conrad_Intro_3`. Complete object comparison
confirmed that only the YarnProject changed in the dialogue asset.
The original English colon-bearing table entry remained exact and
the packaged Ukrainian managed display adapter supplied the visible
body. The fixture was reached by the original menu and virtual
player input. It does not establish entry to the original
`Alexander_2` scene.

Both live TMP components displayed the authored college introduction
with 59 visible non-space glyphs, two lines and no visible speaker
field. Stock choice `line:83ac5b68` advanced to «Александер!» with
11 visible glyphs. The two first-frame full WebP previews showed
legible text, the intact colon and no visible clipping or overlap.
The last two words sit on the second line on both viewports. The
second frame is retained as progression evidence. It has automated
glyph checks and awaits pixel review.

All 172 macOS and 268 CrossOver focus/window samples were `0 0`.
Both test players exited, their original-profile checks passed and
both fixtures kept their initial save bytes. The macOS wrapper
removed its generated Steam file and the test signature verified.

Local sources, copied artifacts and receipts are under
`localization/work/uk-alexander-unity-20261110.Pk2UQe/`.

| Evidence | macOS SHA-256 | Windows SHA-256 |
| --- | --- | --- |
| Fixture dialogue asset | `52961ea6b2095ba5417627acbb736f0b193f9722f3890210d68528d05247a3b7` | `204a43a1e4f08413f9a49b5bc99a7dd922fdd5521cab103ab9666860ee3f94f1` |
| Unity log | `82dbe29b1cfe8e3e520f50906b95534c4c74235f6b6ac576b056cf8da5df1f9a` | `bdf5d19383cf2197cd7a0ddef5d40e627b87cca296f1f24c297b2e55925cef59` |
| Focus and exit receipt | `b8bc26d59c8851047feb9fe3156d3b9191f0d072177c88606fe10e78c53ae508` | `f979fdd095149649f5d878211da2413ad7cdd8b5039f8ce7d340eef7e06185b0` |
| First offscreen PNG | `f09cb1a54d160ffbf5737ab028882855b38fbeace844ec1211ab2030846ea566` | `1535a433de6c5bb5b55cd89bb5b728efc3046f7f475aff751cc10f5467c5dad6` |
| First full WebP80 preview | `dde52b1504d15ae024da0184a19a9d74c97557d3b8d9d63c5ade9f7604258a40` | `bfcc2f816e65bdd213318bc9411ca8ec651192b2b5dadfb2344fc354091bd7fb` |

## Styled choices in Unity

The next fixture also redirected the two AddOption operands in the
first `Conrad_Intro_3` menu. The displayed values are the authored
`line:e104b8e4` and `line:36ff6bd9` from the fourth-batch package.
The fixture retains the original test menu's destinations. The
romance outcomes remain covered separately by the desktop replay.

The stock option views produced matching measurements on both
players. The options had 59 and 106 visible non-space glyphs, with
one and two lines respectively. Both used 36-unit main text and
25.2-unit captions. The presenter interpreted the gradient and size
tags, resolved every observed glyph to its original code point and
reported no TMP overflow. Stock input selected `line:e104b8e4` and
reached «Александер!». Full-frame choice previews are ready for pixel
review, including edge padding and caption readability.

The first macOS attempt stopped at the test's waypoint before
dialogue. The retry raised the window waypoint tolerance from 0.25
to 0.36 world units after a logged approach to 0.269. It retained
the same fixture asset and still required the original window
interaction. The passing macOS and CrossOver runs had 171 and 271
focus/window samples, all `0 0`. The checked profiles and fixture
save bytes matched, and both test players exited.

Local sources and receipts are under
`localization/work/uk-choice-unity-20261110.pFemW7/`.
The accepted macOS run is `mac-retry/run/` and Windows is `win/`.

| Evidence | macOS SHA-256 | Windows SHA-256 |
| --- | --- | --- |
| Fixture dialogue asset | `afa3dab770c1cc064cd1482c143b75708a36dbfca269457d924e93e6e34c4aba` | `27d9192f6cdb448fb17e51a5727162a5f1876b1fb87a6e6821fd8fab08f1765e` |
| Unity log | `0dcf348367fdf68549486ee0ff917b7ed421881c1ebfba42bcaa4a37fdcc0c59` | `ee797eb22008481e6dced29c7db0f2ee41d2bbb01f37e77d4390092c58535994` |
| Focus and exit receipt | `6e4acd7154b8edd4a0a2b57a3675890d9ee5630a2dae3eff49f00f8945e75f8c` | `42924adaef3db811ddbe44c2628f46f730d9b2bdc554a9590f2b4d37959365d3` |
| Option menu offscreen PNG | `7bd23b2b98f0fc7b13c2fd734d0e3f8b77d07eab2f80535c449b7127725cdd0e` | `46b21bfa386eedf4b7dfea0db749cb75c6ff666f70d50a69f37763de0383ad0e` |
| Option menu full WebP80 preview | `2587381f02f41cd5997936812b94ccdc4edecaccc5dada2f336d573350e5ceba` | `d306d9f33756e88a93208e1d01ab37cb5f1f97b72978b499ab921c22e64b72dd` |

Both full option previews were reviewed at their saved dimensions,
640 × 480 and 1074 × 544. The two options and the complete route
captions remained readable, with no visible glyph substitution,
clipping or overlap. The gold lettering is pale on the white panel
and the longer caption wraps close to the right edge. This review
covers these two frames and viewports.

The Ukrainian wording decisions and representative technical
feasibility checks permit ordinary translation. The earlier
[paired script probes](../evidence/european-text-paths-20261110.md)
exercise dialogue, choices and settings. The current fixture covers
the actual protected speaker body and styled choices. Remaining
scene runs, final visual checks and independent editorial review
retain their separate acceptance states.

## First ordinary batch

Both phone tutorials and Ryan's first introduction, wash conversation
and farewell now have all 59 source IDs covered. The draft adds 56
authored values and reuses three special-scene IDs. It contains
463 of 1,947 package IDs with SHA-256
`a54e657aecba9f92fbd97e1b51725489984263fa5fe6b312d9f0c7449e33fda9`.
All 407 previous values are exact.

Both calls use the glossary's branch name and separate the customer
window, gate, crowbar and storage instructions. Ryan's washing
certificate question avoids a gendered player title. Four minor
source variants explicitly share one Ukrainian value across builds.
The two authored ellipses preserve visible pauses.

Both complete builders passed the diagnostic control. The two
packages each changed exactly 54 Yarn values from the fourth-batch
control. The two pauses, the compiled Yarn program and all other
table values and metadata are exact. The packaged fonts cover all 88
display code points used by the draft. This batch's checks are package
read-back and source review. Its gameplay and final editorial checks
remain pending. Receipts are under
`localization/work/uk-ordinary-01-20261110.cvEBPG/`.

## Second ordinary batch

Ryan's second visit now covers all 81 source IDs across arrival,
the wash conversation and farewell. The draft adds 57 values and
reuses 24 special-scene values. The previous 463 values are exact.
The 520-value draft SHA-256 is
`fb210988d11568f666a22b9d64ca74136ad215032f5f20de72d4efd40d1fa3d9`.

The optional farewell keeps the difference between giving Ryan
space and offering to listen. His account retains his girlfriend,
the mud and her reaction, and keeps the repeated player response
at both original branch IDs. The arrival leaves the reference to
markers as stated and preserves the visible pause. The final
source review removed an added degree of muddiness and restored
the explicit thanks for listening before the verified build.

Both diagnostic packages match the authored values. Exactly 56
Yarn values differ from the preceding control. The authored pause,
the other table values and the two compiled programs are exact.
The packaged fonts contain all 89 display code points in the draft.
Live scene checks and independent editorial review remain pending.
The verified receipts are under
`localization/work/uk-ordinary-02-20261110.qDsJDf/reviewed/`.

## Third ordinary batch

Ryan's third visit adds all 50 source IDs across arrival, the wash
conversation and farewell. The draft now covers 570 of 1,947 package
IDs with SHA-256
`49bc7abdc105e7e23fe4a4ecf6644bfe3f0d648219c3274102be61f4282b3621`.
All 520 previous values are exact.

The wording keeps Ryan as the person who ended the relationship,
his account of mutual unhappiness and the distinction between
offering support and responding to the new friendship. His
farewell preserves the scales joke. The two platform spelling and
punctuation variants share Ukrainian values explicitly, and the
small italic hesitation stays in its original span.

The two diagnostic packages each changed exactly 50 Yarn values
from the preceding control. The remaining table text, metadata
and compiled programs are exact. Both packaged fonts contain all
89 display code points. The scope of this batch is source review
and package verification. Its live scene checks and independent
editorial review remain pending. Receipts are under
`localization/work/uk-ordinary-03-20261110.PA4ejz/`.

## Fourth ordinary batch

The fifth visit's shared opening and player–Ryan route now cover
109 source IDs across four nodes. The batch adds 79 values and
reuses 30 from the special-scene wording. The draft covers 649
of 1,947 IDs with SHA-256
`404ab4920814788de0741cf875ae7ba4e206a45a4e948b92c6a872e650bc712a`.
All 570 previous values are exact.

The three diagnostic relationship labels remain distinct. The
opening distinguishes preparing for a date with Conrad, asking
about a date that already happened, and arranging Ryan's date
with the player. The walking, restaurant, bar and film branches
retain their separate choices, including the approved name Wings
and the existing Ukrainian film titles.

Both diagnostic packages changed exactly 79 Yarn values. The
programs, other table text and metadata are exact. Both packaged
fonts contain all 90 display code points used by the draft. The
receipt directory is
`localization/work/uk-ordinary-04-20261110.9IFmem/`.
Live scene checks and independent editorial review remain pending.

## Fifth ordinary batch

The two remaining relationship routes in Ryan's fifth visit add
68 values across the two conversations and their separate
farewells. Two earlier nodes add four lines for a request to come
closer and a refusal to use the device. The draft covers 721 of
1,947 IDs with SHA-256
`38925e6f9a1dcdf25833a92f8f30efa6cb743fbf408a3c4d53e0e8af4e1dda0a`.
All 649 previous values are exact.

The Ryan–Conrad conversation keeps who was hurt, who helped and
who went on the date distinct. The player–Conrad path instead
focuses on Conrad's change in behavior and Ryan's support for the
couple. Common farewell wording retains its separate source IDs.

Each diagnostic package changed exactly 72 Yarn values. The
remaining Yarn text, metadata and programs are exact. Both
packaged fonts contain all 90 display code points. The verified
receipts are under `localization/work/uk-ordinary-05-20261110.7Z6Uc8/`.
Live scene checks and independent editorial review remain pending.
