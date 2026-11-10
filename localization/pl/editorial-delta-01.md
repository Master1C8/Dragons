# Polish draft correction review

This preliminary review binds the first complete draft at `da65676` to
the corrected draft at `0d34c62`. The complete semantic audit and the
independent mandatory regression review retain their separate gates.

The effective paired diff contains only `yarn:line:675d7e37`. Both stock
programs bind the four choices at instructions 406–409 to distinct
answers at 415, 418, 421 and 424, then return to the same line at 426.
The preceding exchange identifies Conrad. The revised Polish option
retains the emphasis, the intended physical implication and its contrast
with the other three options. No other authoring ID has the same full
English source or either exact Polish version.

The coordinator's independent read of this exchange found one follow-up
at `yarn:line:f16d7940`. The reply's `lubią sobie... rekompensować`
shifts a tendency toward enjoyment and leaves an awkward verb
construction. The proposed `Och... Tak, mniejsze smoki zwykle...
nadrabiają.` keeps the habitual meaning and the interrupted joke.
This finding is open for the Polish author. The v2 artifacts and their
runtime evidence still bind the currently committed text.

## Reproduction

```sh
git show da65676:localization/pl/translation.json > "$before"
git show 0d34c62:localization/pl/translation.json > "$after"
"$PYTHON" -B localization/export_editorial_delta.py --locale pl \
  --inventory "$shared_inventory" --yarn-scope "$paired_yarn_scope" \
  --paired-scenes "$paired_scene_export" --before "$before" --after "$after" \
  --recipe localization/pl/editorial-delta-01.json --output "$review_rows"
```

The immutable review export contains 377 target IDs and 55 protected
context records. Its mandatory portion maps the 27 high-risk cases and
all non-Yarn authoring surfaces, with protected credit names and slot
templates retained separately. The changed scene span contains ten
source-bound text positions. The closure ID hash is
`3b95d91ce71975f587c5d5692eed891e92408841f965b277c8f3c7b59dc5f031`
using compact JSON, UTF-8 and one terminating newline.

The two exports reproduced byte for byte. A recipe that omitted the
changed choice from its span failed. An additional effective edit with a
valid snapshot hash but no matching decision also failed. Neither
negative control wrote a review file. The export in
`localization/work/pl-editorial-delta-20261110.iLgOIM/` has SHA-256
`a292c1b2e55e994da869215f9c9e18bdb5939a22840cf76935587e1a6d44c2a8`.
