cd "/Users/fmacchi/Dropbox (MIT)/14.33/ShortProject"

import delimited "exonerations.csv", clear


**Descriptive Statistics of the Data Set**
egen id = group(lastname firstname)
gen yearsWrongfullyConvicted = exonerated - convicted  //length of time between sentencing and exoneration
tab yearsWrongfullyConvicted
tab misdem //3.77% worst crime was a misdeamenor
tab nocrime // 37.06% convicted of crime that NEVER occured

split sentence, destring
replace sentence1="0" if sentence1=="No"
encode sentence1, generate(yearsOfSentence)
drop sentence1

sum yearsWrongfullyConvicted
display r(sum) //29,581 lost years of freedom in the whole dataset

tab sentence //603 sentenced to life/life without parole, 127 Death penalty (and then exonerated)



//One Hot Encoding of the Race Variables
gen black = 1 if race=="Black"
gen white = 1 if race=="White"
gen asian = 1 if race=="Asian"
gen hispanic = 1 if race=="Hispanic"
gen nativeAmer = 1 if race=="Native American"
gen race_Other = 1 if race=="Other"

gen female=1 if sex=="Female"
gen male=1 if sex=="Male"
replace female=0 if missing(female)
replace male=0 if missing(male)


mdesc //Check for missing values
replace black=0 if missing(black)
replace hispanic=0 if missing(hispanic)
replace asian=0 if missing(asian)
replace white=0 if missing(white)
replace nativeAmer=0 if missing(nativeAmer)
replace race_Other=0 if missing(race_Other)


**One Hot Encoding of the Sentences
gen deathSentence = 1 if sentence=="Death"
replace deathSentence=0 if missing(deathSentence)
gen lifeSentence = 1 if sentence=="Life" | sentence=="90 years" | sentence=="95 years" | sentence=="99 years"
replace lifeSentence=0 if missing(lifeSentence)
gen lifeSentenceNoParole = 1 if sentence=="Life without parole"
replace lifeSentenceNoParole=0 if missing(lifeSentenceNoParole)
gen probation = 1 if sentence=="Probation"
replace probation=0 if missing(probation)
gen noSentence = 1 if sentence=="Not sentenced" | sentence=="not sentenced"
replace noSentence=0 if missing(noSentence)

gen otherSentence = 1 if deathSentence==0 & lifeSentence==0 & lifeSentenceNoParole==0 & probation==0 & noSentence==0
replace otherSentence=0 if missing(0)

**One hot encoding of worst crimes 
gen assault = 1 if  worstcrime=="Assault"
replace assault=0 if missing(assault)
gen drugPossession = 1 if  worstcrime=="Drug Possession or Sale"
replace drugPossession=0 if missing(drugPossession)
gen childSexAbuse = 1 if  worstcrime=="Child Sex Abuse"
replace childSexAbuse=0 if missing(childSexAbuse)
gen  murder = 1 if  worstcrime=="Murder"
replace murder=0 if missing(murder)
gen  robbery = 1 if  worstcrime=="Robbery"
replace robbery=0 if missing(robbery)
gen  sexualAssault = 1 if  worstcrime=="Sexual Assault"
replace sexualAssault=0 if missing(sexualAssault)
gen otherCrime = 1 if assault==0 & drugPossession == 0 & childSexAbuse ==0 & murder == 0 & robbery==0 & sexualAssault==0
replace otherCrime=0 if missing(otherCrime)


egen numExonerationsState = count(id), by(statefips) //number of exonerations by state


regress yearsWrongfullyConvicted  black, r
estimates store model1
regress yearsWrongfullyConvicted age male black asian hispanic nativeAmer race_Other,r //baseline covariate for race is White, female for sex
estimates store model2
regress yearsWrongfullyConvicted age male black asian hispanic nativeAmer race_Other i.statefips i.convicted, r //time fixed effects (year of conviction)
estimates store model3
regress yearsWrongfullyConvicted age male black asian hispanic nativeAmer race_Other i.statefips i.convicted assault drugPossession childSexAbuse murder robbery sexualAssault, r
estimates store model4
estwide model1 model2 model3 model4 using /Users/fmacchi/Downloads/exonerations3.tex, se ar2 label keep(age male black asian hispanic nativeAmer race_Other assault drugPossession childSexAbuse murder robbery sexualAssault) title("Relationship Between Race and Sentencing Length")



****************************************************
** Graphs: Further Exploration into Race in the Dataset
****************************************************
bysort exonerated: gen exoneration_countYear = _N
twoway connected exoneration_countYear exonerated if exonerated < 2020, ytitle("Number of Exonerations") title("Exonerations by Year")
