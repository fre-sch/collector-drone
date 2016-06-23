
FilteredCollection = (source, filterModel)->
  filtered = new source.constructor()
  # allow this object to have it's own events
  filtered._callbacks = {}
  filtered.fetch = (options)-> source.fetch(options)

  source.on "reset", ()->
    filtered.reset source.filter(filterModel.where())

  filterModel.on "change", ()->
    items = source.filter filterModel.where()
    filtered.reset items

  filtered
