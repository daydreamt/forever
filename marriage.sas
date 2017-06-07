data marriage2;
	set marriage;
	where (birth_year < 2010 and death_year <= 2017 and birth_year >= 1900 and avg_duration < 70 and avg_duration >= 0);
run;


proc print data=marriage2 (obs=50);
run;

title 'Shortest article sizes';
proc sort data = marriage2 out=marriage_sorted;
by article_size;
run;
proc print data=marriage_sorted (obs=50);
run;

title 'Descriptive statistics';
proc freq data=marriage2;
	TABLES birth_year death_year avg_duration nmarriages;
run;

title 'Means of variables';
proc means data = marriage2;
	var birth_year death_year avg_duration nmarriages;
run;

title 'Jackpot: average duration differs';
proc means data = marriage2;
 var avg_duration;
 class gender;
 output out = quartiles
 p50=median p25=firstquart p75=thirdquart qrange =
interquartilerange;
run;


title 'Long marriages';
proc print data=marriage2;
	where max_duration > 80;
	var name birth_year nmarriages max_duration;
run;



title 'Sex and number of marriages';
proc freq data = marriage2 ;
 tables gender * nmarriages;
run;

title 'Shit data';
proc print data = marriage2;
	where birth_year > 2000;
run;

title 'TODO: Proc tabulate';
proc tabulate data= marriage2;
class gender;
var nmarriages;
table nmarriages;
run;


data marriage_simple;
	set marriage2 (DROP=hec shec);
run;

title 'Subsetting a dataset';
proc print data=marriage_simple (obs = 10);
run;

data marriage_60;
	set marriage_simple;
	if birth_year >= 1960;
	if death_year = '.' then death_year = 2018; /* This is to ensure the next line is correct */
	if death_year-death_year >= max_duration then delete;
	if (1960 <= birth_year and birth_year < 1970) then birth_year=1965;
	else if (1970 <= birth_year and birth_year < 1980) then birth_year=1975;
	else if (1980 <= birth_year and birth_year < 1990) then birth_year=1985;
	else if (1990 <= birth_year and birth_year < 2000) then birth_year=1995;
	else birth_year=2005;
	/*(DROP= death_year);*/
run;

data marriage_60;
	set marriage_60 (drop= death_year);
run;
proc print data=marriage_60 (obs=1000); run;
