class Coordinate(object):
    """
    Class for handling and storing Coordinates.
    For now its just being used for DataSite, but
    in the future we can use it for the GeoData extension.
    """
    def __init__(self, lat, lon, alt=None, precision=None, globe='earth',
                 typ="", name="", dim=None, site=None, entity=''):
        """
        @param lat: Latitude
        @type lat: float
        @param lon: Longitute
        @type lon: float
        @param alt: Altitute? TODO FIXME
        @param precision: precision
        @type precision: float
        @param globe: Which globe the point is on
        @type globe: str
        @param typ: The type of coordinate point
        @type typ: str
        @param name: The name
        @type name: str
        @param dim: Dimension (in meters)
        @type dim: int
        @param entity: The url entity of a Wikibase item
        @type entity: str
        """
        self.lat = lat
        self.lon = lon
        self.alt = alt
        self._precision = precision
        if globe:
            globe = globe.lower()
        self.globe = globe
        self._entity = entity
        self.type = typ
        self.name = name
        self._dim = dim
        if not site:
            self.site = Site().data_repository()
        else:
            self.site = site

    def __repr__(self):
        string = 'Coordinate(%s, %s' % (self.lat, self.lon)
        if self.globe != 'earth':
            string += ', globe="%s"' % self.globe
        string += ')'
        return string

    @property
    def entity(self):
        if self._entity:
            return self._entity
        return self.site.globes()[self.globe]

    def toWikibase(self):
        """
        Function which converts the data to a JSON object
        for the Wikibase API.
        FIXME Should this be in the DataSite object?
        """
        if not self.globe in self.site.globes():
            raise NotImplementedError("%s is not supported in Wikibase yet." % self.globe)
        return {'latitude': self.lat,
                'longitude': self.lon,
                'altitude': self.alt,
                'globe': self.entity,
                'precision': self.precision,
                }

    @staticmethod
    def fromWikibase(data, site):
        """Constructor to create an object from Wikibase's JSON output"""
        globes = {}
        for k in site.globes():
            globes[site.globes()[k]] = k

        globekey = data['globe']
        if globekey:
            globe = globes.get(data['globe'])
        else:
            # Default to earth or should we use None here?
            globe = 'earth'

        return Coordinate(data['latitude'], data['longitude'],
                          data['altitude'], data['precision'],
                          globe, site=site, entity=data['globe'])

    @property
    def precision(self):
        """
        The biggest error (in degrees) will be given by the longitudinal error - the same error in meters becomes larger
        (in degrees) further up north. We can thus ignore the latitudinal error.

        The longitudinal can be derived as follows:

        Therefore: precision = math.degrees( self._dim / ( radius * math.cos( math.radians( self.lat ) ) ) )
        """
        if not self._precision:
            radius = 6378137  # TODO: Support other globes
            self._precision = math.degrees(self._dim / (radius * math.cos(math.radians(self.lat))))
        return self._precision

    def precisionToDim(self):
        """Convert precision from Wikibase to GeoData's dim"""
        raise NotImplementedError
