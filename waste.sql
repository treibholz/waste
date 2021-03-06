CREATE TABLE Dependencies (deleted INTEGER DEFAULT 0, created INTEGER DEFAULT 0, modified INTEGER DEFAULT 0, after INTEGER DEFAULT 0, before INTEGER DEFAULT 0, PRIMARY KEY(before,after,deleted));
CREATE TABLE Priority (deleted INTEGER DEFAULT 0, modified INTEGER, created INTEGER DEFAULT 0, id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE Status (deleted INTEGER DEFAULT 0, created INTEGER DEFAULT 0, modified INTEGER DEFAULT 0, id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE Sync (password TEXT, user TEXT, lastsync INTEGER, remote TEXT);
CREATE TABLE Tagged (modified INTEGER DEFAULT 0, task INTEGER DEFAULT 0, tag INTEGER DEFAULT 0, created INTEGER DEFAULT 0, deleted INTEGER DEFAULT 0, PRIMARY KEY(tag,task,deleted));
CREATE TABLE Tags (deleted INTEGER DEFAULT 0, created INTEGER DEFAULT 0, modified INTEGER DEFAULT 0, id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE Tasks (deleted INTEGER DEFAULT 0, id INTEGER PRIMARY KEY, title TEXT, created INTEGER DEFAULT 0, modified INTEGER DEFAULT 0, priority INTEGER DEFAULT 0, due INTEGER DEFAULT 0, status INTEGER DEFAULT 0);
INSERT INTO "Priority" VALUES(0,0,0,1000,'normal');
INSERT INTO "Status" VALUES(0,0,0,-10,'canceled');
INSERT INTO "Status" VALUES(0,0,0,-1,'done');
INSERT INTO "Status" VALUES(0,0,0,0,'new');
INSERT INTO "Status" VALUES(0,0,0,50,'waiting');
INSERT INTO "Status" VALUES(0,0,0,60,'suspended');
