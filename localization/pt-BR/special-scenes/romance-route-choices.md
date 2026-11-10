# Relationship route choices

Source: paired English worklist and `localization/evidence/special-scenes-romance-20261107.json`. Alexander asks the player on a library date; Conrad asks about people to meet, and Ryan later asks about someone to talk to. The captions distinguish unlocking possible outcomes from confirming a specific route. Author self-reviewed drafts; downstream states, scene context and localized visual fit remain unverified.

| Stable ID | English | Proposed pt-BR |
|---|---|---|
| `yarn:line:a0e49f02` | <gradient="gold"><b> I wouldn't mind! </b></gradient><size=70%> (Will lead to Alexander romance!) | <gradient="gold"><b> Eu toparia! </b></gradient><size=70%> (Leva ao romance com Alexander!) |
| `yarn:line:0371fb9c` | <gradient="gold"><b> I'm going to be busy tonight. Sorry. </b></gradient><size=70%> (Will lead to no romance!) | <gradient="gold"><b> Não vou poder hoje à noite. Desculpe. </b></gradient><size=70%> (Não leva a um romance!) |
| `yarn:line:36ff6bd9` | <gradient="gold"><b> I know a dragon, Ryan. I could get you two in contact? </b></gradient><size=70%>(Unlocks Conrad/Ryan hookup OR Ryan romance) | <gradient="gold"><b> Conheço um dragão, o Ryan. Posso colocar vocês em contato? </b></gradient><size=70%>(Desbloqueia o encontro Conrad/Ryan OU o romance com Ryan) |
| `yarn:line:7e9d40e6` | <gradient="gold"><b> I wouldn't mind hanging out... </b></gradient><size=70%> (Unlocks Conrad romance) | <gradient="gold"><b> Eu toparia passar um tempo com você... </b></gradient><size=70%> (Desbloqueia o romance com Conrad) |
| `yarn:line:bedc761d` | <gradient="gold"><b>I know this one red dragon. I think you'd like him! </b></gradient><size=70%> (Hooks up Ryan with Conrad!) | <gradient="gold"><b> Conheço um dragão vermelho. Acho que você gostaria dele! </b></gradient><size=70%> (Junta Ryan e Conrad!) |
| `yarn:line:e104b8e4` | <gradient="gold"><b>Oh. Uhm. <size=70%> I wouldn't mind... If I was that someone. </b></gradient><size=70%> (Locks in Ryan romance!) | <gradient="gold"><b> Ah. Hum. <size=70%> Eu toparia... Se eu fosse essa pessoa. </b></gradient><size=70%> (Confirma o romance com Ryan!) |
| `yarn:line:f5a81524` | <gradient="gold"><b>I don't have anyone off the top of my head.</b></gradient><size=70%> (Locks in Conrad romance!) | <gradient="gold"><b>Não me vem ninguém à cabeça.</b></gradient><size=70%> (Confirma o romance com Conrad!) |

Retain the exact choice IDs, tag sequence, outcome captions, control variables, conditions and destinations. Test each reachable choice under matching initial state, then verify resulting flags and downstream scenes; do not infer that rejecting Alexander clears earlier state. Review localized choice readability and wrapping on both builds. Complete source discovery and the full preserve-exact contract remain provisional.

## Author decisions after source-gate reconciliation

The author accepts the Alexander and Ryan/Conrad route decisions. Three earlier `Eu adoraria` drafts overstated the source's `I wouldn't mind`; they now use `Eu toparia`, preserving willingness without adding enthusiasm. The captions keep possible unlocks separate from confirmed selections, and the Alexander refusal does not claim to clear any earlier state. All seven target IDs match both platform entries in the fresh paired readback recorded in the checkpoint, including ordered tags. The actual source logic, state guards and original seven choice IDs are documented and tested in the paired original-Yarn VM controls in `localization/evidence/romance-route-analysis-20261107.md`; the per-ID adapter leaves those controls unchanged.

Positive scenarios exercise Alexander's acceptance and refusal with false and previously true state, the suggestion and alternative, and both food-stage relationship menus and their follow-ups. Negative scenarios exchange choices or flags, imply refusal clears earlier Alexander state, or turn an unlock into an immediate exclusive choice. These source controls are not actual Portuguese gameplay. Localized menu fit, flags in the shipped localized build and later scenes remain pending. This is author self-review, not independent acceptance.
