package com.sparkProject

import org.apache.spark.SparkConf
import org.apache.spark.sql.SparkSession
import org.apache.spark.ml.feature.{RegexTokenizer, Tokenizer}
import org.apache.spark.sql.functions._
import org.apache.spark.sql.DataFrame
import org.apache.spark.ml.feature.VectorIndexer
import org.apache.spark.ml.feature.StopWordsRemover
import org.apache.spark.ml.feature.{CountVectorizer, CountVectorizerModel, IDF}
import org.apache.spark.ml.feature.{OneHotEncoder, StringIndexer}
import org.apache.spark.ml.feature.VectorAssembler
import org.apache.spark.ml.Pipeline
import org.apache.spark.ml.classification.LogisticRegression
import org.apache.spark.ml.tuning.{ParamGridBuilder, TrainValidationSplit}
import org.apache.spark.ml.evaluation.MulticlassClassificationEvaluator
//import org.apache.spark.ml.feature.OneHotEncoderEstimator
//import org.apache.spark.ml.feature.ElementWiseProduct


object Trainer {

  def main(args: Array[String]): Unit = {

    val conf = new SparkConf().setAll(Map(
      "spark.scheduler.mode" -> "FIFO",
      "spark.speculation" -> "false",
      "spark.reducer.maxSizeInFlight" -> "48m",
      "spark.serializer" -> "org.apache.spark.serializer.KryoSerializer",
      "spark.kryoserializer.buffer.max" -> "1g",
      "spark.shuffle.file.buffer" -> "32k",
      "spark.default.parallelism" -> "12",
      "spark.sql.shuffle.partitions" -> "12",
      "spark.driver.maxResultSize" -> "2g"
    ))

    val spark = SparkSession
      .builder
      .config(conf)
      .appName("TP_spark")
      .getOrCreate()


    /*******************************************************************************
      *
      *       TP 3
      *
      *       - lire le fichier sauvegarder précédemment
      *       - construire les Stages du pipeline, puis les assembler
      *       - trouver les meilleurs hyperparamètres pour l'entraînement du pipeline avec une grid-search
      *       - Sauvegarder le pipeline entraîné
      *
      *       if problems with unimported modules => sbt plugins update
      *
      ********************************************************************************/

     /* 1. Lire les fichiers parquets */

    val dataset= "/home/karine/Desktop/TELECOM/Spark/prepared_trainingset/*.parquet"
    val df = spark.read.parquet(dataset)



    println("hello world ! from Trainer")
    df.show()
    // -----------------------------------------------------------------------------------------------------------------
    // 2. Utiliser les données textuelles
    // -----------------------------------------------------------------------------------------------------------------
    /* Stage 1 : Separer les textes en mots avec tokenizer */

    val tokenizer = new RegexTokenizer()
      .setPattern("\\W+")
      .setGaps(true)
      .setInputCol("text")
      .setOutputCol("tokens")


    /* Stage 2 : Retirer les stop words  */

    StopWordsRemover.loadDefaultStopWords("english")
    val remover = new StopWordsRemover().setInputCol("tokens").setOutputCol("filtered")

    /* Stage 3 : Convert en TF-IDF */

    val cvModel = new CountVectorizer().setInputCol("filtered").setOutputCol("vectorized")

    /* Stage 4 : Trouver la partie IDF*/

    val idf = new IDF().setInputCol("vectorized").setOutputCol("tfidf")


   //-------------------------------------------------------------------------------------------------------------------
   // 3. Convertir les catégories en données numériques
   //-------------------------------------------------------------------------------------------------------------------

   /* Stage 5 */

   val indexer = new StringIndexer().setInputCol("country2").setOutputCol("country_indexed").setHandleInvalid("skip")

   /* Stage 6 */

   val indexer2=new StringIndexer().setInputCol("currency2").setOutputCol("currency_indexed").setHandleInvalid("skip")

   /* Stage 7 et 8 */

   val encoder=new OneHotEncoder()
     .setInputCol("country_indexed").setOutputCol("country_onehot")

   val encoder2= new OneHotEncoder()
     .setInputCol("currency_indexed").setOutputCol("currency_onehot")



   //-------------------------------------------------------------------------------------------------------------------
   // 4. Mettre les données sous une forme utilisable par SparkML
   //-------------------------------------------------------------------------------------------------------------------
   /* Stage 9 */

   val assembler=new VectorAssembler()
     .setInputCols(Array("tfidf", "days_campaign", "hours_prepa", "goal", "country_onehot","currency_onehot"))
     .setOutputCol("features")

   println("OUTPUT FEATURES")


   /* Stage 10 */

   val lr = new LogisticRegression()
   .setElasticNetParam(0.0)
   .setFitIntercept(true)
   .setFeaturesCol("features")
   .setLabelCol("final_status")
   .setStandardization(true)
   .setPredictionCol("predictions")
   .setRawPredictionCol("raw_predictions")
   .setThresholds(Array(0.7, 0.3))
   .setTol(1.0e-6)
   .setMaxIter(300)

    /* Stage 11 */

   val pipeline = new Pipeline()
      .setStages(Array(tokenizer, remover, cvModel, idf, indexer, indexer2, encoder , encoder2 , assembler, lr))


    //------------------------------------------------------------------------------------------------------------------
    // 5. Entrainer le modèle
    //------------------------------------------------------------------------------------------------------------------

    /* Split data into training (90%) and test (10%). */


    val splits = df.randomSplit(Array(0.9, 0.1), seed = 11L)
    val training = splits(0)
    val test = splits(1)



    /* Grid-search pour trouver les hyperparametres optimaux en utilisant l'évaluateur lr */

    val paramGrid = new ParamGridBuilder()
      .addGrid(lr.regParam, Array(10e-8, 10e-6, 10e-4, 10e-2))
      .addGrid(cvModel.minDF, Array(55.0, 75.0, 95.0))
      .build()

    /* Create the evaluator for a not binary Classification */
    val evaluator = new MulticlassClassificationEvaluator()
      .setMetricName("f1")
      .setLabelCol("final_status")
      .setPredictionCol("predictions")


    /* A TrainValidationSplit requires an Estimator, a set of Estimator ParamMaps, and an Evaluator.*/
    val trainValidationSplit = new TrainValidationSplit()
      .setEstimator(pipeline)
      .setEvaluator(evaluator)
      .setEstimatorParamMaps(paramGrid)
      .setTrainRatio(0.7)

    /* Entrainement du modèle avec l'échantillon training */
    val validationModel = trainValidationSplit.fit(training)

    /* Evaluation modèle avec l'échantillon test*/

    val df_WithPredictions=validationModel.transform(test).select("features","final_status","predictions")
    //df_WithPredictions.show(5)

    val score=evaluator.evaluate(df_WithPredictions)

    df_WithPredictions.groupBy("final_status","predictions").count.show()

    println("F1 Score est " + score)

    /* Save model */
    validationModel.save("/home/karine/Desktop/TELECOM/Spark")


  }
}
