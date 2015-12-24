


// add ask nodes
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:/Users/Zhen/desktop/Courses/Bigdata/stackexchange/data/post.csv" AS row FIELDTERMINATOR ';'
with row
where row.Type='1'
CREATE (:ask {ID: row.ID, Type:row.Type, CreationDate:row.CreationDate, Title:row.Title, Body:row.Body, Tags:row.Tags, ViewCount:row.ViewCount, FavoriteCount:row.FavoriteCount});

// add answer nodes
LOAD CSV WITH HEADERS FROM "file:/Users/Zhen/desktop/Courses/Bigdata/stackexchange/data/post.csv" AS row FIELDTERMINATOR ';'
with row
where  row.Type='2'
CREATE (:answer {ID: row.ID, Type:row.Type, CreationDate:row.CreationDate, Title:row.Title, Body:row.Body, Tags:row.Tags, ViewCount:row.ViewCount, FavoriteCount:row.FavoriteCount});


// add user nodes
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:/Users/Zhen/desktop/Courses/Bigdata/stackexchange/data/user.csv" AS row FIELDTERMINATOR ';'
CREATE (:user {ID: row.ID, Reputation: row.Reputation, CreationDate:row.CreationDate,  Location:row.Location, UpVotes:row.UpVotes, DownVotes:row.DownVotes, Age:row.Age });

// add Tags nodes
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:/Users/Zhen/desktop/Courses/Bigdata/stackexchange/data/tag.csv" AS row FIELDTERMINATOR ';'
CREATE (:tag {ID: row.ID, TagName: row.TagName, TagCount:row.Count});

// add post relation
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:/Users/Zhen/desktop/Courses/Bigdata/stackexchange/data/post_relation.csv" AS row2 FIELDTERMINATOR ';'
MATCH (u:ask),(p:answer)
where  p.ID=row2.START_ID and u.ID=row2.END_ID
MERGE (p) -[t :Answers]-> (u) ;


// add user post relation
USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:/Users/Zhen/desktop/Courses/Bigdata/stackexchange/data/userPoste.csv" AS row2 FIELDTERMINATOR ';'
MATCH (u:user),(p:ask)
where  u.ID=row2.OwnerUserId and p.ID=row2.Id and row2.Type='ask'
MERGE (u) -[t :Ask]-> (p)

USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:/Users/Zhen/desktop/Courses/Bigdata/stackexchange/data/userPoste.csv" AS row2 FIELDTERMINATOR ';'
MATCH (u:user),(p:answer)
WHERE u.ID=row2.OwnerUserId and p.ID=row2.Id and row2.Type='answer'
MERGE (u) -[t :Answer]-> (p)

// add post tag relation
LOAD CSV WITH HEADERS FROM "file:/Users/Zhen/desktop/Courses/Bigdata/stackexchange/data/post_tag_relation_frame.csv" AS row2 FIELDTERMINATOR ';'
MATCH (u:ask),(p:tag)
WHERE u.ID=row2.ID and p.TagName=row2.Tag
MERGE (u) -[t :hasTag]-> (p)

//
MATCH (u:user)-[t:Answer]->(p:ask)
RETURN u, count(*) AS answerCount
ORDER BY answerCount

// find how two tags are connected
MATCH path = allShortestPaths(
     (u:tag {TagName:"r"})-[*]-(me:tag {TagName:"spss"}))
RETURN path;

// find questions that does not have answers yet
MATCH (q:ask)
WHERE NOT (q)<-[:Answer]-(:answer)
RETURN q
