# Waterfall Postcard Studio

Open **File → Waterfall Postcard Studio**, the photo button's **Postcard Studio**
action in either console layout, or its entry in **Station → Features**.
Opening the studio takes a local capture if no draft exists; it never posts.
Keep the main waterfall visible: a minimized/occluded renderer cannot capture
and reports a bounded timeout. Existing Save / Share and Discord buttons remain.

## Make a card

1. **Capture** freezes the rendered spectrum, displayed RF dial, mode, visible
   span, station/grid and UTC acquisition time. Later tuning does not relabel it.
2. Choose **Clean**, **Observatory**, **Tabloid** or **Crab Emergency**. Edit the
   title/caption; **Crab caption** cycles local jokes that you can edit. It uses
   no AI provider or external service.
3. Turn on **Edit crop and annotations**. Drag on the original image to crop,
   circle or draw an arrow; click to place text or the selected crab, UFO,
   monster, goblin stamp or mystery stamp. **Place at center** provides a
   keyboard-accessible placement action. Undo/Clear marks and Reset crop remain
   available. Up to 40 annotations are retained, anchored to original pixels.
4. Optionally select one of the last 100 logged contacts. The card labels the
   contact's own band/mode/date separately from the captured waterfall. Approximate
   distance uses valid station and contact grid centers; missing grids omit it.
   A contact card does not assert that the image captured that contact.
5. Inspect the final card, then **Save / Share**, **Copy PNG**, **Post PNG to
   Discord**, or **Social preview**. Native Save chooses the file location and
   opens the share picker after writing. Discord needs its existing configured
   integration; its diagnostic log records actual delivery. Social preview
   opens Social Announcements and requires its Post button, using enabled,
   configured Mastodon/Bluesky accounts. An existing pending draft is preserved.

## Before and after

Capture the first setup and **Hold as before**. Change the antenna or processing
yourself, then **Capture after**. Both UTC timestamps/frequencies/modes are
retained, the visible-geometry match is labeled, and labels are editable.
A shared crop is applied to both images; annotations decorate the after image.
Images do not calculate or claim a measured noise reduction or signal gain.
Clear comparison to return to a single card or animation.

## Animated waterfalls

Choose 6 or 12 seconds and **Record waterfall GIF**. The studio captures about
two frames per second, with at most 24 encoded frames; actual acquisition
intervals are retained in the GIF. Stop retains completed frames. Source or
receive-geometry changes stop recording before mixing different spans. Closing
the studio stops recording. The main waterfall must remain visible.

**Preview GIF** plays the loop in the studio. **Save animated GIF** selects GIF
for Save / Share; Copy PNG, Discord and Social preview deliberately use the
still card shown by the last capture. GIF has no audio and no IQ recording.
Preview updates after edits return to the still card; use Preview GIF again
to rebuild the animation with the edited recipe.

## Verification boundaries

Production render fixtures exercise all styles, crop/annotation geometry,
contact/comparison layouts, GIF frame count/timing and invalid inputs using
synthetic pixels. Unit tests cover bounded recipes and capture metadata.
Live-radio image acquisition and end-to-end external account delivery require
operator verification. No new transmitter, sample-processing or remote-service
setting is introduced by the studio.
