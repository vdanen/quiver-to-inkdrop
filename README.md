# quiver-to-inkdrop
Script to convert Quiver's json files and import them into CouchDB for Inkdrop to use

This script takes a [Quiver](https://happenapps.com/) library and imports
it directly into a CouchDB server for [Inkdrop](https://inkdrop.app/) to
read.  It sets the document updated/created times properly, retains tags
and notebooks.

I wrote this because Quiver, while allowing me to read my documents in
their mobile clients, won't let me edit them.  Inkdrop has a more robust
mobile experience and is thus more useful to me.

I've successfully imported 1800 Quiver notes from the last few years to
Inkdrop.

# TODO
There are a few limitations that I will try to make better.

- it does not supported nested notebooks from Quiver
- it does not look for attachments; Inkdrop doesn't include attachments but
  there should be a way to call out the attachments (or copy somewhere) and
  tag the notes where they were included so that you can put them on Google
  Docs or Dropbox or somewhere, and link them in the Inkdrop note
- Quiver does more than just markdown but Inkdrop doesn't, so everything
  goes in as Markdown even when it isn't (possibly convert these during
  import?)
- Unknown how this works with Inkdrop's servers; I use a local CouchDB to
  sync to -- it may be possible to update the Inkdrop server directly but
  I've not tried

