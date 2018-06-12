
--
-- CHANGE LOG STARTS

----------------------------------
-- CHANGED IN RHEA 1.0
----------------------------------
-- Column modifierInfo added to dgmEffects
-- Added table dbo.dgmExpressions

----------------------------------
-- CHANGED IN CRIUS 1.0
----------------------------------
-- Removed table invBlueprintTypes (blueprint info now shipped in a separate yaml file)
-- Removed table ramTypeRequirements
-- Removed table ramAssemblyLines
-- Column baseCostMultiplier added to ramAssemblyLineTypes
-- Column costMultiplier added to ramAssemblyLineTypeDetailPerCategory
-- Column costMultiplier added to ramAssemblyLineTypeDetailPerGroup

----------------------------------
-- CHANGED IN RUBICON 1.2
----------------------------------
-- Moved the following tables from the EBS-DUMP (they are now dumped into and sqlite file named universeDataDx.db)
-- dbo.mapDenormalize
-- dbo.mapRegions
-- dbo.mapConstellations
-- dbo.mapSolarSystems
-- dbo.mapLocationScenes
-- dbo.mapLocationWormholeClasses
-- dbo.mapCelestialStatistics
-- dbo.mapJumps
-- dbo.mapSolarSystemJumps
-- dbo.mapConstellationJumps
-- dbo.mapRegionJumps
-- dbo.mapLandmarks
----------------------------------
-- CHANGED IN RUBICON 1.0
----------------------------------
-- Removed table crtCategories
-- Removed table crtClasses
-- Removed table crtRelationships
-- Removed table crtCertificates
-- Removed table crtRecommendations
----------------------------------
-- CHANGED IN RETRIBUTION 1.0.1
----------------------------------
-- Ensured all translated (non-description) string keys are populated.
-- Removed table eveGraphics, it has been replaced by a YAML file named graphicIDs.YAML
-- Removed all FK constraints referencing eveGraphics
-- Removed key invTypes.graphicID, it has been replaced by data in the YAML file named typeIDs.YAML
-- Removed key invTypes.radius, it has been replaced by data in the YAML file named typeIDs.YAML

-- Removed table eveIcons, it has been replaced by a YAML file named iconIDs.YAML
-- Removed all FK constraints referencing eveIcons

-- Removed key iconID from invTypes, it has been replaced by data in the YAML file named typeIDs.YAML
----------------------------------
-- CHANGED IN ESCALATION 1.0
----------------------------------
-- invTypes.marketGroupID changed to int
-- invMarketGroups.marketGroupID changed to int
-- invMarketGroups.parentGroupID changed to int
----------------------------------
-- CHANGED IN CRUCIBLE 1.5
----------------------------------
-- invCategories.categoryID changed to int
-- invGroups.groupID changed to int
-- invGroups.categoryID changed to int
-- invTypes.groupID changed to int
-- mapDenormalize.groupID changed to int
-- ramAssemblyLineTypeDetailPerCategory.categoryID changed to int
-- ramAssemblyLineTypeDetailPerGroup.groupID changed to int
----------------------------------
-- CHANGED IN CRUCIBLE 1.1
----------------------------------
-- Removed table agtConfig, all info should be available in agtAgents
-- Removed table translationLaguages, it should never have existed. Proper name is trnTranslationLanguages.
-- Removed column sceneID from mapLocationScenes and replaced it with graphicID representing the nebula graphic.
----------------------------------
-- CHANGED IN CRUCIBLE
----------------------------------
--
-- Removed table dbo.eveOwners
-- Removed table dbo.eveNames
-- Removed table dbo.eveLocations
-- Added table dbo.invNames
-- Added table dbo.invUniqueNames
-- Added table dbo.invPositions
-- The added tables are not fully compatible with the removed ones as EVE has decided to move away
-- from the item/owner/location paradigm.
-- dbo.invNames contains names of all static items with names.
-- dbo.invUniqueNames contains the names of all entities who have a unique name.
--   It is also seekable on the itemName itself and has a unique constraint on that key.
-- dbo.invPositions contains the (x, y, z) coordinate of static items.
--
--
-- Translation Changes:
-- LanguageID 'EN' changed to 'EN-US'
-- Added table dbo.translationLaguages for all languages that can be found in dbo.trnTranslations
--
--
-- Removed table agtConfig. All info it used to contain is now reflected in agtAgents.
--    Added bit column isLocator to agtAgents to signify wether the agent can locate characters or not.
--
-- Added Tables for Factional Warfare.
--    dbo.warCombatZones
--    dbo.warCombatZoneSystems      
--
-- I knew it! I see way less HTs in pro-tournaments these days!
--
----------------------------------
-- CHANGED IN INCARNA
----------------------------------
-- Added tables:
-- dbo.invItems     := The basic item attributes of all static items
--                     Please see table definition for special handling of quantity key.
-- dbo.eveOwners    := A list of all proper static owners, their names and type
-- dbo.eveLocations := A list of all static locations, their names, types and coordinates.
-- Note: eveOwners and eveLocations are a subset of eveNames. However, only eveNames entries are enforced as unique.
-- 
-- Adding a whole lot of foreign key constraints to signify the relationship between the new tables and the current ones.
-- Seriously.. am I the only one really tired of all the pro-protoss players being so Colossus reliant in every matchup?!
-- And what the fuck is up with the proposed High Templar nerf?! Can we get a colussus nerf so that people at least attempt to find new plays!
--
----------------------------------
-- CHANGED IN TYRANNIS 1.2
----------------------------------
-- All instances of item typeID / groupID / categoryID changed to 32bit ints (Were 16bit / 16bit / 8bit).
-- invFlags.flagID changed from 8bit to 16bit
-- Affected columns:
--    dbo.crtRecommendations.shipTypeID                         -> 32bit
--    dbo.crtRelationships.parentTypeID                         -> 32bit
--    dbo.agtResearchAgents.typeID                              -> 32bit
--    dbo.chrBloodlines.shipTypeID                              -> 32bit
--    dbo.crpNPCCorporationResearchFields.skillID               -> 32bit
--    dbo.crpNPCCorporationTrades.typeID                        -> 32bit
--    dbo.dgmTypeAttributes.typeID                              -> 32bit
--    dbo.dgmTypeEffects.typeID                                 -> 32bit
--    dbo.eveNames.typeID                                       -> 32bit
--    dbo.invBlueprintTypes.blueprintTypeID                     -> 32bit
--    dbo.invBlueprintTypes.parentBlueprintTypeID               -> 32bit
--    dbo.invBlueprintTypes.productTypeID                       -> 32bit
--    dbo.invControlTowerResources.controlTowerTypeID           -> 32bit
--    dbo.invControlTowerResources.resourveTypeID               -> 32bit
--    dbo.invContrabandTypes.typeID                             -> 32bit
--    dbo.invFlags.flagID                                       -> 16bit
--    dbo.invMetaTypes.typeID                                   -> 32bit
--    dbo.invMetaTypes.parentTypeID                             -> 32bit
--    dbo.invTypeReactions.typeID                               -> 32bit
--    dbo.invTypes.typeID                                       -> 32bit
--    dbo.invTypeMaterials.typeID                               -> 32bit
--    dbo.invTypeMaterials.materialTypeID                       -> 32bit
--    dbo.mapDenormalize.typeID                                 -> 32bit
--    dbo.mapSolarSystems.sunTypeID                             -> 32bit
--    dbo.ramInstallationTypeContents.installationTypeID        -> 32bit
--    dbo.ramTypeRequirements.typeID                            -> 32bit
--    dbo.ramTypeRequirements.requiredTypeID                    -> 32bit
--    dbo.ramAssemblyLineStations.stationTypeID                 -> 32bit
--    dbo.staStations.stationTypeID                             -> 32bit
--    dbo.staOperations.caldariStationTypeID                    -> 32bit
--    dbo.staOperations.minmatarStationTypeID                   -> 32bit
--    dbo.staOperations.amarrStationTypeID                      -> 32bit
--    dbo.staOperations.gallenteStationTypeID                   -> 32bit
--    dbo.staOperations.joveStationTypeID                       -> 32bit
--    dbo.staStationTypes.statioTypeID                          -> 32bit
--    dbo.planetSchematicsPinMap.pinTypeID                      -> 32bit
--    dbo.planetSchematicsTypeMap.typeID                        -> 32bit    

----------------------------------
-- CHANGED IN TYRANNIS 1.0.2
----------------------------------
-- NON BACKWARDS COMPATIBLE CHANGES BELOW!
-- Adding table eveIcons for 2D graphics.
-- Table eveGraphics recreated for 3D graphics alone.
-- Removing graphicID (3D) and adding iconID (2D) for the following tables:
--   mapLandmarks, chrAncestries, chrAttributes, chrBloodlines, chrRaces, dgmAttributeTypes, dgmEffects, invCategories, invGroups, invMarketGroups, invMetaGroups, 
-- tables with iconID (2D) added:
--   invTypes, chrFactions, crpNPCCorporations
-- tables that retained graphicID:
--   invTypes


----------------------------------
-- CHANGED IN TYRANNIS
----------------------------------
--- added planetSchematics for planets schematics
--- added planetSchematicsPinMap for mapping of pins to planets schematics
--- added planetSchematicsTypeMap type mapping to planets schematics


----------------------------------
-- CHANGED IN DOMINION
----------------------------------
-- Added crtRecommendations for certificate ship recommendations.
-- Added ramTypeRequirements for requirements for S&I activities
-- Added invTypeMaterials for type material composition
-- Added ramBlueprintTypes for extra blueprint type information
-- Added mapLocationWormholeClasses for wormhole classes. regionID > constellationID > systemID 
--       meaning that if the ID is a region every constellation/system in it has the same ID unless otherwise specified.
-- Added mapLocationScenes which controls what skybox is loaded on what place. locationID := systemID.
-- Removed table typeActivityMaterials, replaced it with the parent tables that create the view.
-- Added table ramInstallationTypeContents for assembly line information of different types.
-- Added table dbo.crpNPCCorporationTrades which lists what NPC corps sell what item.
-- Renamed agtAgents.stationID to locationID. Space pigs will now have a systemID there rather than a NULL.

-- Removed table chrCareers
-- Removed table chrCareerSpecialities
-- Removed table chrRaceSkills
-- Removed table chrSchools
-- Removed table chrSchoolAgents

----------------------------------
-- ADDED IN APOCRYPHA 1.5
----------------------------------
-- Translation support
-- Table trnTranslations contains the translation of text columns into different languages according to languageID
-- Table trnTranslationColumns lists the tcID of a given column in a given table.
-- Added reprocessing information for criminal tags


----------------------------------
-- ADDED IN APOCRYPHA 1.3.1_1
----------------------------------
-- Added skill requirements for certificates to the dump

----------------------------------
-- CHANGED IN APOCRYPHA 1.2
----------------------------------
-- crtCertificates.categoryID changed to tinyint

----------------------------------
-- REMOVED IN APOCRYPHA 1.2
----------------------------------
-- Table chrCareerSkills
-- Table chrCareerSpecialitySkills
-- Careers and Specialities have no impact on skills post-Apocrypha.

----------------------------------
-- ADDED IN APOCRYPHA
----------------------------------
-- KEY ADDITIONS
-- crpNPCCorporations.description
--
--
----------------------------------
-- REMOVED IN APOCRYPHA
----------------------------------
-- invBlueprintTypes.chanceOfReverseEngineering
-- All dgmTypeAttributes records for category = 11 (entities) or group = 988 (wormholes)

----------------------------------
-- ADDED IN QUANTUM RISE
----------------------------------

-- TABLE ADDITIONS
--
-- CERTIFICATES
-- See below for further explanations.
--
-- crtCategories
-- crtClasses
-- crtRelationships
-- crtCertificates


--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
------- FIRST ORDER OF BUSINESS: FREE HONEY FOR EVERYONE! YAY MAYOR BEE! -------
--------------------------------------------------------------------------------
--------------------------------------------------------------------------------


----------------------------------
-- ADDED SINCE EMPYREAN AGE 1.0
----------------------------------

-- FEATURE ADDITIONS
----------------------------------
-- Added Foreign Key definitions
-- NOTE: The dump does NOT come with FKs to facilitate exports into other formats.
-- The definitions are included below for people who'd like to have them. Use whatever find/replace function that supports regex's
-- to remove the comments (or do it manually, your time not mine).
----------------------------------


-- DEFECTS ADDRESSED
----------------------------------
-- Missing table invControlTowerResources added to the dump (was empty).
----------------------------------


-- KEY ADDITIONS
----------------------------------
-- Added recycle bit to typeActivityMaterials
-- 1 := this required materials is reprocessed into it's material components upon the reprocession of the type
--      that requires this material. The reprocessed materials are then added to the material requirements of the
--      type that is being reprocessed (who can be negative) and returned in the reprocess process.
--      Example: Reprocessing a Guardian will reprocess the Augoror required to make a Guardian.
--               These materials are then added to the Augorors bill of materials. Tritanium, for one, is negative in the
--               Augorors BOM so the difference between the two is payed out.
--               Yes, that means you never get the materials used to build the Augoror from the Guardian only the difference between them,
--               the material from the Guardian which was not used to make the Augoror. Funky, huh?
----------------------------------


-- KEY CHANGES
----------------------------------
-- The following keys had their data types changed for the sake of uniformity.
--
-- agtAgents.divisionID is now tinyint
-- chrCareerSpecialities.graphicID is now smallint
-- chrRaces.graphicID is now smallint
-- chrSchools.graphicID is now smallint
-- dgmEffects.falloffAttributeID is now smallint
-- dgmEffects.npcUsageChanceAttributeID is now smallint
-- dgmEffects.npcActivationChanceAttributeID is now smallint
-- dgmEffects.fittingUsageChanceAttributeID is now smallint
-- dgmTypeAttributes.typeID is now smallint
-- dgmTypeEffects.typeID is now smallint
-- eveNames.groupID is now smallint
-- invBlueprintTypes.blueprintTypeID is now smallint
-- invBlueprintTypes.parentBlueprintTypeID is now smallint
-- invBlueprintTypes.productTypeID is now smallint
-- invContrabandTypes.typeID is now smallint
-- invControlTowerResources.controlTowerTypeID is now smallint
-- invControlTowerResources.resourceTypeID is now smallint
-- invMetaTypes.typeID is now smallint
-- invMetaTypes.parentTypeID is now smallint
-- invTypes.groupID is now smallint
-- mapDenormalize.groupID is now smallint
-- staStationTypes.stationTypeID is now smallint
----------------------------------


-- KEY REMOVALS
----------------------------------
-- The following keys are considered legacy data (or just for 3rd party tools) 
-- and were removed to reduce confusion and dump size.
-- chrCareerSpecialities.departmentID
-- chrSchools.agentID
-- crpNPCCorporationDivisions.divisionNumber
-- crpNPCCorporationDivisions.leaderID
-- crpNPCCorporationResearchFields.supplierTypes
-- crpNPCCorporations.mainActivityID;
-- crpNPCCorporations.secondaryActivityID; 
-- dgmAttributeTypes.attributeCategory;
-- dgmAttributeTypes.attributeIdx;
-- dgmAttributeTypes.maxAttributeID;
-- dgmAttributeTypes.chargeRechargeTimeID; 

----------------------------------

--
-- CHANGE LOG ENDS
--

-- TRANSLATIONS
-- trnTranslations
IF OBJECT_ID ('dbo.trnTranslations') IS NOT NULL
  DROP TABLE dbo.trnTranslations
GO
CREATE TABLE dbo.trnTranslations
(
  tcID        smallint       NOT NULL,
  keyID       int            NOT NULL,
  languageID  varchar(50)    NOT NULL,
  [text]      nvarchar(max)  NOT NULL,
  
  CONSTRAINT trnTranslations_PK PRIMARY KEY CLUSTERED(tcID, keyID, languageID)
)
GO

-- trnTranslationColumns
IF OBJECT_ID ('dbo.trnTranslationColumns') IS NOT NULL
  DROP TABLE dbo.trnTranslationColumns
GO
CREATE TABLE dbo.trnTranslationColumns
(
  tcGroupID      smallint       NULL,
  tcID           smallint       NOT NULL,
  tableName      nvarchar(256)  NOT NULL,
  columnName     nvarchar(128)  NOT NULL,
  masterID       nvarchar(128)  NULL,

  CONSTRAINT translationColumns_PK PRIMARY KEY CLUSTERED (tcID)
)
GO

-- translationLaguages
IF OBJECT_ID('dbo.trnTranslationLanguages') IS NOT NULL
  DROP TABLE dbo.trnTranslationLanguages
GO
CREATE TABLE dbo.trnTranslationLanguages
(
    numericLanguageID   int            NOT NULL,
    languageID          varchar(50)    NULL,
    languageName        nvarchar(200)  NULL,
    
    CONSTRAINT trnTranslationLanguages_PK PRIMARY KEY CLUSTERED (numericLanguageID) 
)
GO

-- planet schematics tables
IF OBJECT_ID ('dbo.planetSchematics') IS NOT NULL
  DROP TABLE dbo.planetSchematics
GO
CREATE TABLE dbo.planetSchematics
(
  schematicID     smallint,
  schematicName   nvarchar(255),
  cycleTime       int,

  CONSTRAINT planetSchematics_PK PRIMARY KEY CLUSTERED (schematicID)
)
GO

IF OBJECT_ID ('dbo.planetSchematicsPinMap') IS NOT NULL
  DROP TABLE dbo.planetSchematicsPinMap
GO
CREATE TABLE dbo.planetSchematicsPinMap
(
  schematicID     smallint,
  pinTypeID       int,

  CONSTRAINT planetSchematicsPinMap_PK PRIMARY KEY CLUSTERED (schematicID, pinTypeID)
)
GO

IF OBJECT_ID ('dbo.planetSchematicsTypeMap') IS NOT NULL
  DROP TABLE dbo.planetSchematicsTypeMap
GO
CREATE TABLE dbo.planetSchematicsTypeMap
(
  schematicID     smallint,
  typeID          int,
  quantity        smallint,
  isInput         bit,

  CONSTRAINT planetSchematicsTypeMap_PK PRIMARY KEY CLUSTERED (schematicID, typeID)
)
GO

-- AGENTS
-- Agents
IF OBJECT_ID('dbo.agtAgents') IS NOT NULL
  DROP TABLE dbo.agtAgents
GO
CREATE TABLE dbo.agtAgents
(
  agentID        int,
  divisionID     tinyint,
  corporationID  int,
  locationID     int,
  [level]        tinyint,
  quality        smallint,
  agentTypeID    int,
  isLocator      bit,

  CONSTRAINT agtAgents_PK PRIMARY KEY CLUSTERED (agentID)
)
CREATE NONCLUSTERED INDEX agtAgents_IX_corporation ON agtAgents (corporationID)
CREATE NONCLUSTERED INDEX agtAgents_IX_station ON agtAgents (locationID)
GO

-- Research agents and their fields
-- This is new. If agent has a science skill it can research that field.
IF OBJECT_ID('dbo.agtResearchAgents') IS NOT NULL
  DROP TABLE dbo.agtResearchAgents
GO
CREATE TABLE dbo.agtResearchAgents
(
  agentID      int,
  typeID       int,

  CONSTRAINT agtResearchAgents_PK PRIMARY KEY CLUSTERED (agentID, typeID)
)
CREATE NONCLUSTERED INDEX agtResearchAgents_IX_type ON dbo.agtResearchAgents (typeID)
GO

-- Agent Types
IF OBJECT_ID('dbo.agtAgentTypes') IS NOT NULL
  DROP TABLE dbo.agtAgentTypes
GO
CREATE TABLE dbo.agtAgentTypes
(
  agentTypeID  int,
  agentType    varchar(50),
  
  CONSTRAINT agtAgentTypes_PK PRIMARY KEY CLUSTERED (agentTypeID)
)
GO


-- CHARACTER
-- Character creation relevant tables.
-- Ancestries
IF OBJECT_ID('dbo.chrAncestries') IS NOT NULL
  DROP TABLE dbo.chrAncestries
GO
CREATE TABLE dbo.chrAncestries
(
  ancestryID        tinyint,
  ancestryName      nvarchar(100),
  bloodlineID       tinyint,
  description       nvarchar(1000),
  perception        tinyint,
  willpower         tinyint,
  charisma          tinyint,
  memory            tinyint,
  intelligence      tinyint,
  iconID            int,
  shortDescription  nvarchar(500),

  CONSTRAINT chrAncestries_PK PRIMARY KEY CLUSTERED (ancestryID)
)
GO

-- Attributes
IF OBJECT_ID('dbo.chrAttributes') IS NOT NULL
  DROP TABLE dbo.chrAttributes
GO
CREATE TABLE dbo.chrAttributes
(
  attributeID       tinyint,
  attributeName     varchar(100),
  description       varchar(1000),
  iconID            int,
  shortDescription  nvarchar(500),
  notes             nvarchar(500),

  CONSTRAINT chrAttributes_PK PRIMARY KEY CLUSTERED (attributeID)
)
GO

-- Bloodlines
IF OBJECT_ID('dbo.chrBloodlines') IS NOT NULL
  DROP TABLE dbo.chrBloodlines
GO
CREATE TABLE dbo.chrBloodlines
(
  bloodlineID             tinyint,
  bloodlineName           nvarchar(100),
  raceID                  tinyint,
  description             nvarchar(1000),
  maleDescription         nvarchar(1000),
  femaleDescription       nvarchar(1000),
  shipTypeID              int,
  corporationID           int,

  perception              tinyint,
  willpower               tinyint,
  charisma                tinyint,
  memory                  tinyint,
  intelligence            tinyint,

  iconID                  int,       

  shortDescription        nvarchar(500),
  shortMaleDescription    nvarchar(500),
  shortFemaleDescription  nvarchar(500),

  CONSTRAINT chrBloodlines_PK PRIMARY KEY CLUSTERED (bloodlineID)
)
GO

-- Factions
IF OBJECT_ID('dbo.chrFactions') IS NOT NULL
  DROP TABLE dbo.chrFactions
GO
CREATE TABLE dbo.chrFactions
(
  factionID             int,
  factionName           varchar(100),
  description           varchar(1000),
  raceIDs               int,
  solarSystemID         int,
  corporationID         int,
  sizeFactor            float,
  stationCount          smallint,
  stationSystemCount    smallint,
  militiaCorporationID  int,
  iconID                int,

  CONSTRAINT chrFactions_PK PRIMARY KEY CLUSTERED (factionID)
)
GO

-- Races
IF OBJECT_ID('dbo.chrRaces') IS NOT NULL
  DROP TABLE dbo.chrRaces
GO
CREATE TABLE dbo.chrRaces
(
  raceID            tinyint,
  raceName          varchar(100),
  description       varchar(1000),
  iconID            int,
  shortDescription  varchar(500),

  CONSTRAINT chrRaces_PK PRIMARY KEY CLUSTERED (raceID)  
)
GO

-- CORPORATIONS
-- Activities
IF OBJECT_ID('dbo.crpActivities') IS NOT NULL
  DROP TABLE dbo.crpActivities
GO
CREATE TABLE dbo.crpActivities
(
  activityID      tinyint,
  activityName    nvarchar(100),
  description     nvarchar(1000),

  CONSTRAINT crpActivities_PK PRIMARY KEY CLUSTERED (activityID)
)
GO


-- crpNPCCorporationDivisions
IF OBJECT_ID('dbo.crpNPCCorporationDivisions') IS NOT NULL
  DROP TABLE dbo.crpNPCCorporationDivisions
GO
CREATE TABLE dbo.crpNPCCorporationDivisions
(
  corporationID   int,
  divisionID      tinyint,
  [size]          tinyint,

  CONSTRAINT crpNPCCorporationDivisions_PK PRIMARY KEY CLUSTERED (corporationID, divisionID)
)
GO


-- Research Fields
IF OBJECT_ID('dbo.crpNPCCorporationResearchFields') IS NOT NULL
  DROP TABLE dbo.crpNPCCorporationResearchFields
GO
CREATE TABLE dbo.crpNPCCorporationResearchFields
(
  skillID        int,
  corporationID  int,

  CONSTRAINT crpNPCCorporationResearchFields_PK PRIMARY KEY CLUSTERED (skillID, corporationID)
)
GO


-- NPCCorporations
IF OBJECT_ID('dbo.crpNPCCorporations') IS NOT NULL
  DROP TABLE dbo.crpNPCCorporations
GO
CREATE TABLE dbo.crpNPCCorporations
(
  corporationID        int,
  [size]               char(1),
  extent               char(1),
  solarSystemID        int,
  investorID1          int,     
  investorShares1      tinyint,
  investorID2          int,
  investorShares2      tinyint,
  investorID3          int,
  investorShares3      tinyint,
  investorID4          int,
  investorShares4      tinyint,
  friendID             int,
  enemyID              int,
  publicShares         bigint,
  initialPrice         int,
  minSecurity          float,
  scattered            bit,
  fringe               tinyint,
  corridor             tinyint,
  hub                  tinyint,
  border               tinyint,
  factionID            int,
  sizeFactor           float,
  stationCount         smallint,
  stationSystemCount   smallint,
  description          nvarchar(4000),
  iconID               int,

  CONSTRAINT crpNPCCorporations_PK PRIMARY KEY CLUSTERED (corporationID)
)
GO

-- Divisions
IF OBJECT_ID('dbo.crpNPCDivisions') IS NOT NULL
  DROP TABLE dbo.crpNPCDivisions
GO
CREATE TABLE dbo.crpNPCDivisions
(
  divisionID    tinyint,
  divisionName  nvarchar(100),
  description   nvarchar(1000),
  leaderType    nvarchar(100),

  CONSTRAINT crpNPCDivisions_PK PRIMARY KEY CLUSTERED (divisionID)
)
GO

-- Trade info
IF OBJECT_ID('dbo.crpNPCCorporationTrades') IS NOT NULL
  DROP TABLE dbo.crpNPCCorporationTrades
GO
CREATE TABLE dbo.crpNPCCorporationTrades
(
  corporationID  int,
  typeID         int,
  
  CONSTRAINT crpNPCCorporationTrades_PK PRIMARY KEY CLUSTERED (corporationID, typeID)
)
GO



-- DOGMA
-- Attributes
IF OBJECT_ID('dbo.dgmAttributeTypes') IS NOT NULL
  DROP TABLE dbo.dgmAttributeTypes
GO
CREATE TABLE dbo.dgmAttributeTypes
(
  attributeID           smallint,
  attributeName         varchar(100),
  description           varchar(1000),
  iconID                int,
  defaultValue          float,
  published             bit,
  displayName           varchar(100),
  unitID                tinyint,
  stackable             bit,
  highIsGood            bit,
  categoryID            tinyint,

  CONSTRAINT dgmAttributeTypes_PK PRIMARY KEY CLUSTERED (attributeID)  
)
GO

-- Attribute categories
-- Included for convenience, has zero game effect.
IF OBJECT_ID('dbo.dgmAttributeCategories') IS NOT NULL
  DROP TABLE dbo.dgmAttributeCategories
GO
CREATE TABLE dbo.dgmAttributeCategories
(
    categoryID           tinyint,
    categoryName         nvarchar(50),
    categoryDescription  nvarchar(200),  

  CONSTRAINT dgmAttributeCategories_PK PRIMARY KEY CLUSTERED (categoryID)
)
GO

-- Type Attributes
IF OBJECT_ID('dbo.dgmTypeAttributes') IS NOT NULL
  DROP TABLE dbo.dgmTypeAttributes
GO
CREATE TABLE dbo.dgmTypeAttributes
(
  typeID       int,
  attributeID  smallint,
  valueInt     int,
  valueFloat   float,

  CONSTRAINT dgmTypeAttributes_PK PRIMARY KEY CLUSTERED (typeID, attributeID)
)
GO

-- Expressions
IF OBJECT_ID('dbo.dgmExpressions') IS NOT NULL
  DROP TABLE dbo.dgmExpressions
GO
CREATE TABLE dbo.dgmExpressions
(
  expressionID           int,
  operandID              int,
  arg1                   int,
  arg2                   int,
  expressionValue        varchar(100),
  description            varchar(1000),
  expressionName         varchar(500),
  expressionTypeID       int,
  expressionGroupID      smallint,
  expressionAttributeID  smallint,
  --
  CONSTRAINT dgmExpressions_PK PRIMARY KEY CLUSTERED (expressionID)
)

-- Effects
IF OBJECT_ID('dbo.dgmEffects') IS NOT NULL
  DROP TABLE dbo.dgmEffects
GO
CREATE TABLE dbo.dgmEffects
(
  effectID                        smallint,
  effectName                      varchar(400) COLLATE Latin1_General_CI_AI,
  effectCategory                  smallint,
  preExpression                   int,
  postExpression                  int,
  description                     varchar(1000),
  guid                            varchar(60),
  iconID                          int,
  isOffensive                     bit,
  isAssistance                    bit,
  durationAttributeID             smallint,
  trackingSpeedAttributeID        smallint,
  dischargeAttributeID            smallint,
  rangeAttributeID                smallint,
  falloffAttributeID              smallint,
  disallowAutoRepeat              bit,
  published                       bit,
  displayName                     varchar(100),
  isWarpSafe                      bit,
  rangeChance                     bit,
  electronicChance                bit,
  propulsionChance                bit,
  distribution                    tinyint,
  sfxName                         varchar(20),
  npcUsageChanceAttributeID       smallint,
  npcActivationChanceAttributeID  smallint,
  fittingUsageChanceAttributeID   smallint,
  modifierInfo                    varchar(max),

  CONSTRAINT dgmEffects_PK PRIMARY KEY CLUSTERED (effectID)
)
GO

-- Type Effects
IF  OBJECT_ID('dbo.dgmTypeEffects') IS NOT NULL
  DROP TABLE dbo.dgmTypeEffects
GO
CREATE TABLE dbo.dgmTypeEffects
(
  typeID      int,
  effectID    smallint,
  isDefault   bit,

  CONSTRAINT dgmTypeEffects_PK PRIMARY KEY CLUSTERED(typeID, effectID)
)
GO


-- EVE
-- Owner
IF OBJECT_ID('dbo.eveOwners') IS NOT NULL
  DROP TABLE dbo.eveOwners
GO

-- Locations
IF OBJECT_ID('dbo.eveLocations') IS NOT NULL
  DROP TABLE dbo.eveLocations
GO

-- Icons
IF OBJECT_ID('dbo.eveIcons') IS NOT NULL
  DROP TABLE dbo.eveIcons
GO

IF OBJECT_ID('dbo.eveGraphics') IS NOT NULL
  DROP TABLE dbo.eveGraphics
GO


-- Names
IF OBJECT_ID('dbo.eveNames') IS NOT NULL
  DROP TABLE dbo.eveNames
GO

-- Units
IF OBJECT_ID('dbo.eveUnits') IS NOT NULL
  DROP TABLE dbo.eveUnits
GO
CREATE TABLE dbo.eveUnits
(
  unitID       tinyint,
  unitName     varchar(100),
  displayName  varchar(50),
  description  varchar(1000),

  CONSTRAINT eveUnits_PK PRIMARY KEY CLUSTERED (unitID)
)
GO


-- POS
-- Control Tower Resources
IF OBJECT_ID('dbo.invControlTowerResources') IS NOT NULL
  DROP TABLE dbo.invControlTowerResources
GO
CREATE TABLE dbo.invControlTowerResources
(
  controlTowerTypeID  int,
  resourceTypeID      int,
  --
  purpose             tinyint,
  quantity            int,
  minSecurityLevel    float,
  factionID           int,

  CONSTRAINT invControlTowerResources_PK PRIMARY KEY CLUSTERED (controlTowerTypeID, resourceTypeID)
)
GO


-- INVENTORY
-- POS Resource Purpose
IF OBJECT_ID('dbo.invControlTowerResourcePurposes') IS NOT NULL
  DROP TABLE dbo.invControlTowerResourcePurposes
GO
CREATE TABLE dbo.invControlTowerResourcePurposes
(
  purpose      tinyint,
  purposeText  varchar(100),
  --
  CONSTRAINT invControlTowerResourcePurposes_PK PRIMARY KEY CLUSTERED (purpose)
)
GO

IF OBJECT_ID('dbo.invItems') IS NOT NULL
  DROP TABLE dbo.invItems
GO
CREATE TABLE dbo.invItems
(
    itemID      bigint    NOT NULL,
    typeID      int       NOT NULL,
    ownerID     int       NOT NULL,
    locationID  bigint    NOT NULL,
    flagID      smallint  NOT NULL,
    quantity    int       NOT NULL,  -- Attention! quantity = -1 signifies a non-stackable item with a quantity of 1
                                     -- where as quantity = 1 signifies a stackable item with a quantity of 1
    --
    CONSTRAINT invItems_PK PRIMARY KEY CLUSTERED (itemID)
)
CREATE NONCLUSTERED INDEX items_IX_Location ON invItems (locationID)
CREATE NONCLUSTERED INDEX items_IX_OwnerLocation ON invItems (ownerID, locationID)
GO

IF OBJECT_ID('dbo.invUniqueNames') IS NOT NULL
  DROP TABLE dbo.invUniqueNames
GO
CREATE TABLE dbo.invUniqueNames
(
  itemID    int                                          NOT NULL,
  itemName  nvarchar(200)  COLLATE Latin1_General_CI_AI  NOT NULL,
  --
  groupID   int                                          NULL,
  --
  CONSTRAINT invUniqueNames_PK PRIMARY KEY CLUSTERED (itemID)
)
CREATE UNIQUE NONCLUSTERED INDEX invUniqueNames_UQ ON dbo.invUniqueNames (itemName)
CREATE NONCLUSTERED INDEX invUniqueNames_IX_GroupName ON dbo.invUniqueNames (groupID, itemName)
GO

IF OBJECT_ID('dbo.invNames') IS NOT NULL
  DROP TABLE dbo.invNames
GO
CREATE TABLE dbo.invNames
(
    itemID     bigint         NOT NULL,
    itemName   nvarchar(200)  NOT NULL,
    
    CONSTRAINT invNames_PK PRIMARY KEY CLUSTERED (itemID)
)
GO

IF OBJECT_ID('dbo.invPositions') IS NOT NULL
  DROP TABLE dbo.invPositions
GO
CREATE TABLE dbo.invPositions
(
    itemID  bigint  NOT NULL,
    x       float   NOT NULL  DEFAULT 0.0,
    y       float   NOT NULL  DEFAULT 0.0,
    z       float   NOT NULL  DEFAULT 0.0,
    yaw     real    NULL,
    pitch   real    NULL,
    roll    real    NULL,
    --
    CONSTRAINT invPositions_PK PRIMARY KEY CLUSTERED (itemID)
)
GO

-- Categories
IF OBJECT_ID('dbo.invCategories') IS NOT NULL
  DROP TABLE dbo.invCategories
GO
CREATE TABLE dbo.invCategories
(
  categoryID    int,
 
  categoryName  nvarchar(100)   COLLATE Latin1_General_CI_AI,
  description   nvarchar(3000),
  iconID        int,
  published     bit,

  CONSTRAINT invCategories_PK PRIMARY KEY CLUSTERED (categoryID)
)
GO

-- Contraband
IF OBJECT_ID('dbo.invContrabandTypes') IS NOT NULL
  DROP TABLE dbo.invContrabandTypes
GO
CREATE TABLE dbo.invContrabandTypes
(
  factionID         int,
  typeID            int,

  standingLoss      float,
  confiscateMinSec  float,
  fineByValue       float,
  attackMinSec      float,

  CONSTRAINT invContrabandTypes_PK PRIMARY KEY CLUSTERED (factionID, typeID)
)
  CREATE NONCLUSTERED INDEX invContrabandTypes_IX_type ON dbo.invContrabandTypes (typeID)
GO

-- Flags
IF OBJECT_ID('dbo.invFlags') IS NOT NULL
  DROP TABLE dbo.invFlags
GO
CREATE TABLE dbo.invFlags
(
  flagID    smallint,
  flagName  varchar(200),
  flagText  varchar(100),
  orderID   int,

  CONSTRAINT invFlags_PK PRIMARY KEY CLUSTERED (flagID)
)
GO

-- Groups
IF OBJECT_ID('dbo.invGroups') IS NOT NULL
  DROP TABLE dbo.invGroups
GO
CREATE TABLE dbo.invGroups
(
  groupID               int,
  --
  categoryID            int,
  groupName             nvarchar(100)   COLLATE Latin1_General_CI_AI,
  description           nvarchar(3000),
  iconID                int,
  useBasePrice          bit,
  allowManufacture      bit,
  allowRecycler         bit,
  anchored              bit,
  anchorable            bit,
  fittableNonSingleton  bit,
  published             bit,
  
  CONSTRAINT invGroups_PK PRIMARY KEY CLUSTERED (groupID)
)
  CREATE NONCLUSTERED INDEX invGroups_IX_category ON dbo.invGroups (categoryID)
GO


-- Market groups
IF OBJECT_ID('dbo.invMarketGroups') IS NOT NULL
  DROP TABLE dbo.invMarketGroups
GO
CREATE TABLE dbo.invMarketGroups
(
  marketGroupID    int,
  --
  parentGroupID    int,
  marketGroupName  nvarchar(100),
  description      nvarchar(3000),
  iconID           int,
  hasTypes         bit,

  CONSTRAINT invMarketGroups_PK PRIMARY KEY CLUSTERED (marketGroupID)
)
GO

-- Meta Groups
IF OBJECT_ID('dbo.invMetaGroups') IS NOT NULL
  DROP TABLE dbo.invMetaGroups
GO
CREATE TABLE dbo.invMetaGroups
(
  metaGroupID    smallint,
  --
  metaGroupName  nvarchar(100),
  description    nvarchar(1000),
  iconID         int,

  CONSTRAINT invMetaGroups_PK PRIMARY KEY CLUSTERED (metaGroupID)
)
GO

-- Meta Types
IF OBJECT_ID('dbo.invMetaTypes') IS NOT NULL
  DROP TABLE dbo.invMetaTypes
GO
CREATE TABLE dbo.invMetaTypes
(
  typeID        int,
  --
  parentTypeID  int,
  metaGroupID   smallint,

  CONSTRAINT invMetaTypes_PK PRIMARY KEY CLUSTERED(typeID)
)
GO

-- Type Reactions
IF OBJECT_ID('dbo.invTypeReactions') IS NOT NULL
  DROP TABLE dbo.invTypeReactions
GO
CREATE TABLE dbo.invTypeReactions
(
  reactionTypeID  int,
  input           bit,
  typeID          int,
  quantity        smallint,
  --
  CONSTRAINT pk_invTypeReactions PRIMARY KEY CLUSTERED (reactionTypeID, input, typeID)
)


-- Types
IF OBJECT_ID('dbo.invTypes') IS NOT NULL
  DROP TABLE dbo.invTypes
GO
CREATE TABLE dbo.invTypes
(
  typeID               int,
  groupID              int,
  typeName             nvarchar(100)   COLLATE Latin1_General_CI_AI,
  description          nvarchar(3000),
  mass                 float,
  volume               float,
  capacity             float,
  portionSize          int,
  raceID               tinyint,
  basePrice            money,
  published            bit,
  marketGroupID        int,
  chanceOfDuplicating  float
                                 
  CONSTRAINT invTypes_PK PRIMARY KEY CLUSTERED (typeID)
)
CREATE NONCLUSTERED INDEX invTypes_IX_Group ON dbo.invTypes (groupID)
GO


IF OBJECT_ID('dbo.invTypeMaterials') IS NOT NULL
  DROP TABLE dbo.invTypeMaterials
CREATE TABLE dbo.invTypeMaterials
(
  typeID          int  NOT NULL,
  materialTypeID  int  NOT NULL,
  --
  quantity        int  NOT NULL  DEFAULT 0,
  --
  CONSTRAINT invTypeMaterials_PK PRIMARY KEY CLUSTERED (typeID, materialTypeID)
)


-- Universe
IF OBJECT_ID('dbo.mapUniverse') IS NOT NULL
  DROP TABLE dbo.mapUniverse
GO
CREATE TABLE dbo.mapUniverse
(
  universeID    int,
  universeName  varchar(100),
  x             float,
  y             float,
  z             float,
  xMin          float,
  xMax          float,
  yMin          float,
  yMax          float,
  zMin          float,
  zMax          float,
  radius        float,
  --
  CONSTRAINT mapUniverse_PK PRIMARY KEY CLUSTERED (universeID)
)
GO


-- RAM
IF OBJECT_ID('dbo.ramInstallationTypeContents') IS NOT NULL
  DROP TABLE dbo.ramInstallationTypeContents
CREATE TABLE dbo.ramInstallationTypeContents
(
  installationTypeID  int      NOT NULL,
  assemblyLineTypeID  tinyint  NOT NULL,
  --
  quantity            tinyint  NULL,
  CONSTRAINT ramInstallationTypeContents_PK PRIMARY KEY CLUSTERED (installationTypeID, assemblyLineTypeID)
)
GO


-- Activities
IF OBJECT_ID('dbo.ramActivities') IS NOT NULL
  DROP TABLE dbo.ramActivities
GO
CREATE TABLE dbo.ramActivities
(
  activityID     tinyint,
  activityName   nvarchar(100),
  iconNo         varchar(5),
  description    nvarchar(1000),
  published      bit,
  --
  CONSTRAINT ramActivities_PK PRIMARY KEY CLUSTERED (activityID)
)
GO


-- Assembly Lines by Station
IF OBJECT_ID('dbo.ramAssemblyLineStations') IS NOT NULL
  DROP TABLE dbo.ramAssemblyLineStations
GO
CREATE TABLE dbo.ramAssemblyLineStations
(
  stationID           int,
  assemblyLineTypeID  tinyint,
  quantity            tinyint,
  stationTypeID       int,
  ownerID             int,
  solarSystemID       int,
  regionID            int,
  --
  CONSTRAINT ramAssemblyLineStations_PK PRIMARY KEY CLUSTERED (stationID, assemblyLineTypeID)
)
CREATE NONCLUSTERED INDEX ramAssemblyLineStations_IX_region ON ramAssemblyLineStations (regionID)
CREATE NONCLUSTERED INDEX ramAssemblyLineStations_IX_owner ON ramAssemblyLineStations (ownerID)

GO


-- Assembly Line Type Details Per Category
IF OBJECT_ID('dbo.ramAssemblyLineTypeDetailPerCategory') IS NOT NULL
  DROP TABLE dbo.ramAssemblyLineTypeDetailPerCategory
GO
CREATE TABLE dbo.ramAssemblyLineTypeDetailPerCategory
(
  assemblyLineTypeID  tinyint,
  categoryID          int,
  timeMultiplier      float,
  materialMultiplier  float,
  costMultiplier      float,
  --
  CONSTRAINT ramAssemblyLineTypeDetailPerCategory_PK PRIMARY KEY CLUSTERED (assemblyLineTypeID, categoryID)
)
GO


-- ramAssemblyLineTypeDetailPerGroup
IF OBJECT_ID('dbo.ramAssemblyLineTypeDetailPerGroup') IS NOT NULL
  DROP TABLE dbo.ramAssemblyLineTypeDetailPerGroup
GO
CREATE TABLE dbo.ramAssemblyLineTypeDetailPerGroup
(
  assemblyLineTypeID  tinyint,
  groupID             int,
  timeMultiplier      float,
  materialMultiplier  float,
  costMultiplier      float,
  --
  CONSTRAINT ramAssemblyLineTypeDetailPerGroup_PK PRIMARY KEY CLUSTERED (assemblyLineTypeID, groupID)
)
GO

-- Assembly Line Types
IF OBJECT_ID('dbo.ramAssemblyLineTypes') IS NOT NULL
  DROP TABLE dbo.ramAssemblyLineTypes
GO
CREATE TABLE dbo.ramAssemblyLineTypes
(
  assemblyLineTypeID      tinyint,
  assemblyLineTypeName    nvarchar(100),
  description             nvarchar(1000),
  baseTimeMultiplier      float,
  baseMaterialMultiplier  float,
  baseCostMultiplier      float,
  volume                  float,
  activityID              tinyint,
  minCostPerHour          float,
  --
  CONSTRAINT ramAssemblyLineTypes_PK PRIMARY KEY CLUSTERED (assemblyLineTypeID)
)
GO

-- STATIONS
-- Operations
IF OBJECT_ID('dbo.staOperations') IS NOT NULL
  DROP TABLE dbo.staOperations
GO
CREATE TABLE dbo.staOperations
(
  activityID             tinyint,
  operationID            tinyint,
  operationName          nvarchar(100),
  description            nvarchar(1000),
  fringe                 tinyint,
  corridor               tinyint,
  hub                    tinyint,
  border                 tinyint,
  ratio                  tinyint,
  caldariStationTypeID   int,
  minmatarStationTypeID  int,
  amarrStationTypeID     int,
  gallenteStationTypeID  int,
  joveStationTypeID      int,
  --
  CONSTRAINT staOperations_PK PRIMARY KEY CLUSTERED (operationID)
)
GO

-- Operation Services
IF OBJECT_ID('dbo.staOperationServices') IS NOT NULL
  DROP TABLE dbo.staOperationServices
GO
CREATE TABLE dbo.staOperationServices
(
  operationID  tinyint,
  serviceID    int,
  --
  CONSTRAINT staOperationServices_PK PRIMARY KEY CLUSTERED (operationID, serviceID)
)
GO

-- Services
IF OBJECT_ID('dbo.staServices') IS NOT NULL
  DROP TABLE dbo.staServices
GO
CREATE TABLE dbo.staServices
(
  serviceID    int,
  serviceName  nvarchar(100),
  description  nvarchar(1000),
  --
  CONSTRAINT staServices_PK PRIMARY KEY CLUSTERED (serviceID)
)
GO


-- Stations
IF OBJECT_ID('dbo.staStations') IS NOT NULL
  DROP TABLE dbo.staStations
GO
CREATE TABLE dbo.staStations
(
  stationID                 int,
  [security]                smallint,
  dockingCostPerVolume      float,
  maxShipVolumeDockable     float,
  officeRentalCost          int,
  operationID               tinyint,
  -- DENORMALIZED DATA
  stationTypeID             int,
  corporationID             int,
  solarSystemID             int,
  constellationID           int,
  regionID                  int,
  stationName               nvarchar(100)  COLLATE Latin1_General_CI_AI,
  x                         float,
  y                         float,
  z                         float,
  reprocessingEfficiency    float,
  reprocessingStationsTake  float,
  reprocessingHangarFlag    tinyint,
  --
  CONSTRAINT staStations_PK PRIMARY KEY CLUSTERED (stationID)
)
CREATE NONCLUSTERED INDEX staStations_IX_region ON staStations (regionID)
CREATE NONCLUSTERED INDEX staStations_IX_system ON staStations (solarSystemID)
CREATE NONCLUSTERED INDEX staStations_IX_constellation ON staStations (constellationID)
CREATE NONCLUSTERED INDEX staStations_IX_operation ON staStations (operationID)
CREATE NONCLUSTERED INDEX staStations_IX_type ON staStations (stationTypeID)
CREATE NONCLUSTERED INDEX staStations_IX_corporation ON staStations (corporationID)
GO

-- Types
IF OBJECT_ID('dbo.staStationTypes') IS NOT NULL
  DROP TABLE dbo.staStationTypes
GO
CREATE TABLE dbo.staStationTypes
(
  stationTypeID           int,
  --
  dockEntryX              float,
  dockEntryY              float,
  dockEntryZ              float,
  dockOrientationX        float,
  dockOrientationY        float,
  dockOrientationZ        float,
  operationID             tinyint,
  officeSlots             tinyint,
  reprocessingEfficiency  float,
  conquerable             bit,
  --
  CONSTRAINT stationTypes_PK PRIMARY KEY CLUSTERED (stationTypeID)
)
GO

-- Factional Warfare
IF OBJECT_ID('dbo.warCombatZones') IS NOT NULL
  DROP TABLE dbo.warCombatZones
GO
CREATE TABLE dbo.warCombatZones
(
  combatZoneID    int            NOT NULL DEFAULT -1,
  combatZoneName  nvarchar(100)  NULL,
  factionID       int            NULL,
  centerSystemID  int            NULL,
  description     nvarchar(500)  NULL,
  CONSTRAINT combatZones_PK PRIMARY KEY CLUSTERED (combatZoneID)
)
GO

IF OBJECT_ID('dbo.warCombatZoneSystems') IS NOT NULL
  DROP TABLE dbo.warCombatZoneSystems
GO
CREATE TABLE dbo.warCombatZoneSystems
(
  solarSystemID  int      NOT NULL,
  combatZoneID   int      NULL,

  CONSTRAINT combatZoneSystems_PK PRIMARY KEY CLUSTERED (solarSystemID)    
)
GO


---
--- FOREIGN KEYS
---

/*

ALTER TABLE agtAgents ADD CONSTRAINT agtAgents_FK_agent FOREIGN KEY (agentID) REFERENCES invNames(itemID)
ALTER TABLE agtAgents ADD CONSTRAINT agtAgents_FK_division FOREIGN KEY (divisionID) REFERENCES crpNPCDivisions(divisionID)
ALTER TABLE agtAgents ADD CONSTRAINT agtAgents_FK_corporation FOREIGN KEY (corporationID) REFERENCES crpNPCCorporations(corporationID)
ALTER TABLE agtAgents ADD CONSTRAINT agtAgents_FK_agentType FOREIGN KEY (agentTypeID) REFERENCES agtAgentTypes(agentTypeID)

ALTER TABLE agtResearchAgents ADD CONSTRAINT agtResearchAgents_FK_agent FOREIGN KEY (agentID) REFERENCES agtAgents(agentID)
ALTER TABLE agtResearchAgents ADD CONSTRAINT agtResearchAgents_FK_type FOREIGN KEY (typeID) REFERENCES invTypes(typeID)

ALTER TABLE chrBloodlines ADD CONSTRAINT chrBloodlines_FK_shipType FOREIGN KEY (shipTypeID) REFERENCES invTypes(typeID)
ALTER TABLE chrBloodlines ADD CONSTRAINT chrBloodlines_FK_corporation FOREIGN KEY (corporationID) REFERENCES crpNPCCorporations(corporationID)

ALTER TABLE chrFactions ADD CONSTRAINT chrFactions_FK_faction FOREIGN KEY (factionID) REFERENCES invNames(itemID)
ALTER TABLE chrFactions ADD CONSTRAINT chrFactions_FK_solarSystem FOREIGN KEY (solarSystemID) REFERENCES mapSolarSystems(solarSystemID)
ALTER TABLE chrFactions ADD CONSTRAINT chrFactions_FK_corporationID FOREIGN KEY (corporationID) REFERENCES crpNPCCorporations(corporationID)
ALTER TABLE chrFactions ADD CONSTRAINT chrFactions_FK_militiaCorporationID FOREIGN KEY (militiaCorporationID) REFERENCES crpNPCCorporations(corporationID)

ALTER TABLE crpNPCCorporationDivisions ADD CONSTRAINT crpNPCCorporationDivisions_FK_corporation FOREIGN KEY (corporationID) REFERENCES crpNPCCorporations(corporationID)
ALTER TABLE crpNPCCorporationDivisions ADD CONSTRAINT crpNPCCorporationDivisions_FK_division FOREIGN KEY (divisionID) REFERENCES crpNPCDivisions(divisionID)

ALTER TABLE crpNPCCorporationResearchFields ADD CONSTRAINT crpNPCCorporationResearchFields_FK_skill FOREIGN KEY (skillID) REFERENCES invTypes(typeID)
ALTER TABLE crpNPCCorporationResearchFields ADD CONSTRAINT crpNPCCorporationResearchFields_FK_corporatioin FOREIGN KEY (corporationID) REFERENCES crpNPCCorporations(corporationID)

ALTER TABLE dbo.crpNPCCorporationTrades ADD CONSTRAINT crpNPCCorporationTrades_FK_corporation FOREIGN KEY (corporationID) REFERENCES dbo.crpNPCCorporations(corporationID)
ALTER TABLE dbo.crpNPCCorporationTrades ADD CONSTRAINT crpNPCCorporationTrades_FK_type FOREIGN KEY (typeID) REFERENCES dbo.invTypes(typeID)

ALTER TABLE crpNPCCorporations ADD CONSTRAINT crpNPCCorporations_FK_corporation FOREIGN KEY (corporationID) REFERENCES invNames(itemID)
ALTER TABLE crpNPCCorporations ADD CONSTRAINT crpNPCCorporations_FK_solarSystem FOREIGN KEY (solarSystemID) REFERENCES mapSolarSystems(solarSystemID)
ALTER TABLE crpNPCCorporations ADD CONSTRAINT crpNPCCorporations_FK_investor1 FOREIGN KEY (investorID1) REFERENCES crpNPCCorporations(corporationID)
ALTER TABLE crpNPCCorporations ADD CONSTRAINT crpNPCCorporations_FK_investor2 FOREIGN KEY (investorID2) REFERENCES crpNPCCorporations(corporationID)
ALTER TABLE crpNPCCorporations ADD CONSTRAINT crpNPCCorporations_FK_investor3 FOREIGN KEY (investorID3) REFERENCES crpNPCCorporations(corporationID)
ALTER TABLE crpNPCCorporations ADD CONSTRAINT crpNPCCorporations_FK_investor4 FOREIGN KEY (investorID4) REFERENCES crpNPCCorporations(corporationID)
ALTER TABLE crpNPCCorporations ADD CONSTRAINT crpNPCCorporations_FK_friend FOREIGN KEY (friendID) REFERENCES crpNPCCorporations(corporationID)
ALTER TABLE crpNPCCorporations ADD CONSTRAINT crpNPCCorporations_FK_enemy FOREIGN KEY (enemyID) REFERENCES crpNPCCorporations(corporationID)
ALTER TABLE crpNPCCorporations ADD CONSTRAINT crpNPCCorporations_FK_faction FOREIGN KEY (factionID) REFERENCES chrFactions(factionID)

ALTER TABLE dgmAttributeTypes ADD CONSTRAINT dgmAttributeTypes_FK_unit FOREIGN KEY (unitID) REFERENCES eveUnits(unitID)
ALTER TABLE dgmAttributeTypes ADD CONSTRAINT dgmAttributeTypes_FK_category FOREIGN KEY (categoryID) REFERENCES dgmAttributeCategories(categoryID)

ALTER TABLE dgmTypeAttributes ADD CONSTRAINT dgmTypeAttributes_FK_type FOREIGN KEY (typeID) REFERENCES invTypes(typeID)
ALTER TABLE dgmTypeAttributes ADD CONSTRAINT dgmTypeAttributes_FK_attribute FOREIGN KEY (attributeID) REFERENCES dgmAttributeTypes(attributeID)

ALTER TABLE dgmEffects ADD CONSTRAINT dgmEffects_FK_durationAttribute FOREIGN KEY (durationAttributeID) REFERENCES dgmAttributeTypes(attributeID)
ALTER TABLE dgmEffects ADD CONSTRAINT dgmEffects_FK_trackingSpeedAttribute FOREIGN KEY (trackingSpeedAttributeID) REFERENCES dgmAttributeTypes(attributeID)
ALTER TABLE dgmEffects ADD CONSTRAINT dgmEffects_FK_dischargeAttribute FOREIGN KEY (dischargeAttributeID) REFERENCES dgmAttributeTypes(attributeID)
ALTER TABLE dgmEffects ADD CONSTRAINT dgmEffects_FK_rangeAttribute FOREIGN KEY (rangeAttributeID) REFERENCES dgmAttributeTypes(attributeID)
ALTER TABLE dgmEffects ADD CONSTRAINT dgmEffects_FK_falloffAttribute FOREIGN KEY (falloffAttributeID) REFERENCES dgmAttributeTypes(attributeID)
ALTER TABLE dgmEffects ADD CONSTRAINT dgmEffects_FK_npcUsageChanceAttributeID FOREIGN KEY (npcUsageChanceAttributeID) REFERENCES dgmAttributeTypes(attributeID)
ALTER TABLE dgmEffects ADD CONSTRAINT dgmEffects_FK_npcActivationChanceAttributeID FOREIGN KEY (npcActivationChanceAttributeID) REFERENCES dgmAttributeTypes(attributeID)
ALTER TABLE dgmEffects ADD CONSTRAINT dgmEffects_FK_fittingUsageChanceAttributeID FOREIGN KEY (fittingUsageChanceAttributeID) REFERENCES dgmAttributeTypes(attributeID)

ALTER TABLE dgmTypeEffects ADD CONSTRAINT dgmTypeEffects_FK_type FOREIGN KEY (typeID) REFERENCES invTypes(typeID)
ALTER TABLE dgmTypeEffects ADD CONSTRAINT dgmTypeEffects_FK_effects FOREIGN KEY (effectID) REFERENCES dgmEffects(effectID)

ALTER TABLE invUniqueNames ADD CONSTRAINT invUniqueNames_FK_item FOREIGN KEY (itemID) REFERENCES invItems(itemID)
ALTER TABLE invUniqueNames ADD CONSTRAINT invUniqueNames_FK_group FOREIGN KEY (groupID) REFERENCES invGroups(groupID)

ALTER TABLE invPositions ADD CONSTRAINT invPositions_FK_location FOREIGN KEY (itemID) REFERENCES invItems(itemID)

ALTER TABLE invNames ADD CONSTRAINT invNames_FK_item FOREIGN KEY (itemID) REFERENCES invItems(itemID)

ALTER TABLE invControlTowerResources ADD CONSTRAINT invControlTowerResources_FK_faction FOREIGN KEY (factionID) REFERENCES chrFactions(factionID)
ALTER TABLE invControlTowerResources ADD CONSTRAINT invControlTowerResources_FK_resourceType FOREIGN KEY (resourceTypeID) REFERENCES invTypes(typeID)
ALTER TABLE invControlTowerResources ADD CONSTRAINT invControlTowerResources_FK_constrolTowerType FOREIGN KEY (controlTowerTypeID) REFERENCES invTypes(typeID)

ALTER TABLE invContrabandTypes ADD CONSTRAINT invContrabandTypes_FK_type FOREIGN KEY (typeID) REFERENCES invTypes(typeID)
ALTER TABLE invContrabandTypes ADD CONSTRAINT invContrabandTypes_FK_faction FOREIGN KEY (factionID) REFERENCES chrFactions(factionID)

ALTER TABLE invGroups ADD CONSTRAINT invGroups_FK_category FOREIGN KEY (categoryID) REFERENCES invCategories(categoryID)

ALTER TABLE invMarketGroups ADD CONSTRAINT invMarketGroups_FK_parentGroup FOREIGN KEY (parentGroupID) REFERENCES invMarketGroups(marketGroupID)

ALTER TABLE invMetaTypes ADD CONSTRAINT invMetaTypes_FK_type FOREIGN KEY (typeID) REFERENCES invTypes(typeID)
ALTER TABLE invMetaTypes ADD CONSTRAINT invMetaTypes_FK_parentType FOREIGN KEY (parentTypeID) REFERENCES invTypes(typeID)
ALTER TABLE invMetaTypes ADD CONSTRAINT invMetaTypes_FK_metaGroup FOREIGN KEY (metaGroupID) REFERENCES invMetaGroups(metaGroupID)

ALTER TABLE invTypeReactions ADD CONSTRAINT invTypeReactions_FK_type FOREIGN KEY (typeID) REFERENCES invTypes(typeID)

ALTER TABLE invTypes ADD CONSTRAINT invTypes_FK_group FOREIGN KEY (groupID) REFERENCES invGroups(groupID)
ALTER TABLE invTypes ADD CONSTRAINT invTypes_FK_race FOREIGN KEY (raceID) REFERENCES chrRaces(raceID)
ALTER TABLE invTypes ADD CONSTRAINT invTypes_FK_marketGroup FOREIGN KEY (marketGroupID) REFERENCES invMarketGroups(marketGroupID)

ALTER TABLE ramAssemblyLineStations ADD CONSTRAINT ramAssemblyLineStations_FK_station FOREIGN KEY (stationID) REFERENCES staStations(stationID)
ALTER TABLE ramAssemblyLineStations ADD CONSTRAINT ramAssemblyLineStations_FK_assemblyLineType FOREIGN KEY (assemblyLineTypeID) REFERENCES ramAssemblyLineTypes(assemblyLineTypeID)
ALTER TABLE ramAssemblyLineStations ADD CONSTRAINT ramAssemblyLineStations_FK_owner FOREIGN KEY (ownerID) REFERENCES crpNPCCorporations(corporationID)
ALTER TABLE ramAssemblyLineStations ADD CONSTRAINT ramAssemblyLineStations_FK_stationType FOREIGN KEY (stationTypeID) REFERENCES staStationTypes(stationTypeID)
ALTER TABLE ramAssemblyLineStations ADD CONSTRAINT ramAssemblyLineStations_FK_solarSystem FOREIGN KEY (solarSystemID) REFERENCES mapSolarSystems(solarSystemID)
ALTER TABLE ramAssemblyLineStations ADD CONSTRAINT ramAssemblyLineStations_FK_region FOREIGN KEY (regionID) REFERENCES mapRegions(regionID)

ALTER TABLE ramAssemblyLineTypeDetailPerCategory ADD CONSTRAINT ramAssemblyLineTypeDetailPerCategory_FK_assemblyLineType FOREIGN KEY (assemblyLineTypeID) REFERENCES ramAssemblyLineTypes(assemblyLineTypeID)
ALTER TABLE ramAssemblyLineTypeDetailPerCategory ADD CONSTRAINT ramAssemblyLineTypeDetailPerCategory_FK_category FOREIGN KEY (categoryID) REFERENCES invCategories(categoryID)

ALTER TABLE ramAssemblyLineTypeDetailPerGroup ADD CONSTRAINT ramAssemblyLineTypeDetailPerGroup_FK_assemblyLineType FOREIGN KEY (assemblyLineTypeID) REFERENCES ramAssemblyLineTypes(assemblyLineTypeID)
ALTER TABLE ramAssemblyLineTypeDetailPerGroup ADD CONSTRAINT ramAssemblyLineTypeDetailPerGroup_FK_group FOREIGN KEY (groupID) REFERENCES invGroups(groupID)

ALTER TABLE ramAssemblyLineTypes ADD CONSTRAINT ramAssemblyLineTypes_FK_activity FOREIGN KEY (activityID) REFERENCES ramActivities(activityID)

ALTER TABLE staOperations ADD CONSTRAINT staOperations_FK_activity FOREIGN KEY (activityID) REFERENCES crpActivities(activityID)
ALTER TABLE staOperations ADD CONSTRAINT staOperations_FK_caldariStationType FOREIGN KEY (caldariStationTypeID) REFERENCES invTypes(typeID)
ALTER TABLE staOperations ADD CONSTRAINT staOperations_FK_minmatarStationType FOREIGN KEY (minmatarStationTypeID) REFERENCES invTypes(typeID)
ALTER TABLE staOperations ADD CONSTRAINT staOperations_FK_amarrStationType FOREIGN KEY (amarrStationTypeID) REFERENCES invTypes(typeID)
ALTER TABLE staOperations ADD CONSTRAINT staOperations_FK_gallenteStationType FOREIGN KEY (gallenteStationTypeID) REFERENCES invTypes(typeID)
ALTER TABLE staOperations ADD CONSTRAINT staOperations_FK_joveStationType FOREIGN KEY (joveStationTypeID) REFERENCES invTypes(typeID)

ALTER TABLE staOperationServices ADD CONSTRAINT staOperationServices_FK_operation FOREIGN KEY (operationID) REFERENCES staOperations(operationID)
ALTER TABLE staOperationServices ADD CONSTRAINT staOperationServices_FK_service FOREIGN KEY (serviceID) REFERENCES staServices(serviceID)

ALTER TABLE staStationTypes ADD CONSTRAINT staStationTypes_FK_stationType FOREIGN KEY (stationTypeID) REFERENCES invTypes(typeID)

ALTER TABLE staStations ADD CONSTRAINT staStations_FK_station FOREIGN KEY (stationID) REFERENCES invPositions(itemID)
ALTER TABLE staStations ADD CONSTRAINT staStations_FK_operation FOREIGN KEY (operationID) REFERENCES staOperations(operationID)
ALTER TABLE staStations ADD CONSTRAINT staStations_FK_type FOREIGN KEY (stationTypeID) REFERENCES staTypes(stationTypeID)
ALTER TABLE staStations ADD CONSTRAINT staStations_FK_corporation FOREIGN KEY (corporationID) REFERENCES crpNPCCorporations(corporationID)
ALTER TABLE staStations ADD CONSTRAINT staStations_FK_solarSystem FOREIGN KEY (solarSystemID) REFERENCES mapSolarSystems(solarSystemID)
ALTER TABLE staStations ADD CONSTRAINT staStation_FK_constellation FOREIGN KEY (constellationID) REFERENCES mapConstellations(constellationID)
ALTER TABLE staStations ADD CONSTRAINT staStationd_FK_region FOREIGN KEY (regionID) REFERENCES mapRegions(regionID)

ALTER TABLE dbo.invTypeMaterials ADD CONSTRAINT invTypeMaterials_FK_type FOREIGN KEY (typeID) REFERENCES invTypes(typeID)
ALTER TABLE dbo.invTypeMaterials ADD CONSTRAINT invTypeMaterials_FK_materialType FOREIGN KEY (typeID) REFERENCES invTypes(typeID)
*/