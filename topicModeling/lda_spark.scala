import org.apache.spark.mllib.clustering.{LDA, DistributedLDAModel}
import org.apache.spark.mllib.linalg.Vectors

// Load and parse the data
val data = sc.textFile("/Users/Zhen/Desktop/Courses/BigData/stackexchange/topicModeling/result/matrix0.csv")

val parsedData = data.map(s => Vectors.dense(s.trim.split(',').map(_.toDouble)))
// Index documents with unique IDs
val corpus = parsedData.zipWithIndex.map(_.swap).cache()

// Cluster the documents into three topics using LDA
val numTopics = 10
val lda = new LDA().setK(numTopics).setMaxIterations(10)
val ldaModel = lda.run(corpus)

// then convert to distributed LDA model
val distLDAModel = ldaModel.asInstanceOf[DistributedLDAModel]
val topicDist = distLDAModel.topicDistributions
ldaModel.describeTopics()
topicDist.toDF()
topicDist.saveAsTextFile("/Users/Zhen/desktop/Courses/Bigdata/stackexchange/topicModeling/result/topicDist.txt")


