library(ggplot2)
library(nlme)
library(lme4)
library(sjPlot)
library(performance)
library(effects)
library(brms)
library(posterior)
library(R2jags)
library(rstan)
library(knitr)
library(olsrr)
library(DHARMa)
library(lmer)
library(performance)
library(effects)


#ouvrir le DF
DF <- read.csv("C:/Users/iuiui/Downloads/TEST_fixation_exclude_c.tsv")

#regarder la structure du df
summary(DF)

#boxplot pour la durée totale de fixation par condition
hist(DF$Total_duration_of_whole_fixations., main = "Distribution of Total Fixation Duration")
boxplot(Total_duration_of_whole_fixations. ~ condition, data = DF, main = "Durée totale de fixation par condition")

#boxplot pour la durée moyenne de fixation par condition
hist(DF$Average_duration_of_whole_fixations., main = "Distribution of Average Fixation Duration")
boxplot(Average_duration_of_whole_fixations. ~ condition, data = DF, main = "Durée moyenne de fixation par condition")

#boxplot pour la durée moyenne de fixation par condition
hist(DF$Number_of_whole_fixations., main = "Distribution of number of Fixation")
boxplot(Number_of_whole_fixations. ~ condition, data = DF, main = "Nombres de fixation par condition")


#faire un plot complet 
par(mfrow = c(2, 3))  # 2 lignes, 3 colonnes

# première ligne : Histograms
hist(DF$Total_duration_of_whole_fixations., main = "Distribution de la durée totale de fixation")
hist(DF$Average_duration_of_whole_fixations., main = "Distribution des durées moyennes de fixation")
hist(DF$Number_of_whole_fixations., main = "Distribution du nombre de fixation")

# deuxième ligne: Boxplots
boxplot(Total_duration_of_whole_fixations. ~ condition, data = DF, main = "Durée totale de fixation par condition")
boxplot(Average_duration_of_whole_fixations. ~ condition, data = DF, main = "Durée moyenne de fixation par condition")
boxplot(Number_of_whole_fixations. ~ condition, data = DF, main = "Nombre de fixation par condition")

par(mfrow = c(1, 1))


#créer un LMM qui regarde la durée totale de fixation selon la condition et l'item
model_total_duration_condition_item <- lmer(Total_duration_of_whole_fixations. ~ condition + (1|item), data = DF)

#s'assurer de la normalité du modèle

#OK: residuals appear as normally distributed (p = 0.288).
check_normality(model_total_duration_condition_item) 

#dans notre cas : Warning: Heteroscedasticity (non-constant error variance) detected (p < .001). --> à étudier !
check_heteroscedasticity(model_total_duration_condition_item) 

#pour observer les outliers, ici : 4 outliers detected: cases 25, 39, 43, 45.
# - Based on the following method and threshold: cook (0.5).
# - For variable: (Whole model).
check_outliers(model_total_duration_condition_item) 

#plot du modèle et de l'effet PT VS. QM
plot(allEffects(model_total_duration_condition_item))


#créer un LMM qui regarde la durée totale de fixation selon la condition et l'item, et l'AOI
model_total_duration_condition_item_AOI <- lmer(Total_duration_of_whole_fixations. ~ condition + (1|item) + (1|AOI), data = DF)

#d'abord il y a eu : boundary (singular) fit: see help('isSingular')
# à faire : ajouter le nombre de lettre dans l'AOI pour chaque item + aoi

#test
model_total_AOI <- lmer(Total_duration_of_whole_fixations. ~ condition + (1|AOI), data = DF)

#test modèle croisé durée totale ~ AOI+item
library(brms)
model_bayes_Total_item_AOI <- brm(Total_duration_of_whole_fixations. ~ condition + 
                     (1|item) + (1|AOI),
                   data = DF,
                   chains = 4, iter = 2000)