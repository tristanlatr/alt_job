
<h1 align="center">Alt Job</h1>

<p align="center">
  Scraping alternative websites for jobs.
  <br>
</p>

<p align="center">
  <a href="https://github.com/tristanlatr/alt_job/actions" target="_blank"><img src="https://github.com/tristanlatr/alt_job/workflows/test/badge.svg"></a>
  <a href="https://pypi.org/project/alt-job/" target="_blank"><img src="https://badge.fury.io/py/alt-job.svg"></a>
  <!-- <a href="https://codecov.io/gh/tristanlatr/alt_job" target="_blank"><img src="https://codecov.io/gh/tristanlatr/alt_job/branch/master/graph/badge.svg"></a> -->
  <!-- <a href="https://codeclimate.com/github/tristanlatr/alt_job" target="_blank"><img src="https://codeclimate.com/github/tristanlatr/alt_job/badges/gpa.svg"></a> -->

</p>

Atl Job scrapes a bunch of green/social/alternative websites to send digest of new job postings by email. Also generates an Excel file with job postings informations.   

The scraped data include: **job title, type, salary, week_hours, date posted, apply before date and full description**.  Additionnaly, a set of [keywords matches](https://github.com/tristanlatr/alt_job/blob/master/alt_job/pipelines.py) are automatically checked against all jobs and added as a new column.  (See [screens](https://github.com/tristanlatr/alt_job/blob/master/screens))  

This project is still under construction! 🚧

### Job postings mailling lists  🔥

-  Montréal / Québec:  
[alt_job_mtl](https://groups.google.com/forum/?utm_medium=email&utm_source=footer#!forum/alt_job_mtl) Google Group. Join to receive a daily digest of new Montréal and Province of Québec job postings.  

### Supported websites

Alt Job is wrote in an extensible way, only 30 lines of code are required to support a new job posting site! Focused on Canada/Québec for now, please [contribute](https://github.com/tristanlatr/alt_job/blob/master/CONTRIBUTE.md) to improve the software or expand the scope 🙂

Supports the following websites: 
- [arrondissement.com](https://www.arrondissement.com/montreal-list-emplois/t1/pc1/): Québec (full parsing) 
- [cdeacf.ca](http://cdeacf.ca/recherches/offre_demploi): Québec (full job PDFs parsing) 
- [chantier.qc.ca](https://chantier.qc.ca/decouvrez-leconomie-sociale/offres-demploi/): Québec  (full parsing)   
- [goodwork.ca](https://www.goodwork.ca): Québec and Canada (full parsing, form search still TODO)  
- [engages.ca](https://www.engages.ca): Québec (paging TODO)  
- [enviroemplois.org](https://www.enviroemplois.org): Québec (full parsing)  
- [charityvillage.com](https://charityvillage.com): Québec and Canada (full parsing, require chromedriver)  
- [aqoci.qc.ca](https://www.aqoci.qc.ca/?-emplois-et-benevolat-): Québec, Internationnal (full parsing)


The support of the following websites is on the TODO:   
- [undpjobs.net](https://undpjobs.net/country/Canada): World Wide
- [eco.ca]()
- [novae.ca]()
- [quebecmunicipal.qc.ca]()

### Install

*Install all requirements (see [setup.py](https://github.com/tristanlatr/alt_job/blob/master/setup.py) for more details)*
```bash
python3 -m pip install 'alt_job[all]'
```

Require Python >= 3.6  

### Configure

Sample config file
```ini


[alt_job]

##### General config #####

# Logging
log_level=INFO
scrapy_log_level=ERROR

# Jobs data file, default is ~/jobs.json
# jobs_datafile=/home/user/Jobs/jobs-mtl.json

# Asynchronous workers, number of site to scan at the same time
# Default to 5.
# workers=10

##### Mail sender #####

# Email server settings
smtphost=smtp.gmail.com
mailfrom=you@gmail.com
smtpuser=you@gmail.com
smtppass=password
smtpport=587
smtptls=Yes

# Email notif settings
mailto=["you@gmail.com"]

##### Scrapers #####

# Website domain
[goodwork.ca]
# URL to start the scraping, required for all scrapers
url=https://www.goodwork.ca/jobs.php?prov=QC

[cdeacf.ca]
url=http://cdeacf.ca/recherches?f%5B0%5D=type%3Aoffre_demploi

# Load full jobs details: If supported by the scraper,
#   this will follow each job posting link in listing and parse full job description.
#   turn on to parse all job informations
# Default to False!
load_full_jobs=True

[arrondissement.com]
url=https://www.arrondissement.com/tout-list-emplois/

# Load all new pages: If supported by the scraper,
#   this will follow each "next page" links and parse next listing page
#   until older (in database) job postings are found.
# Default to False!
load_all_new_pages=True

[chantier.qc.ca]
url=https://chantier.qc.ca/decouvrez-leconomie-sociale/offres-demploi
load_full_jobs=Yes

# Disabled scraper
# [engages.ca]
# url=https://www.engages.ca/emplois?search%5Bkeyword%5D=&search%5Bjob_sector%5D=&search%5Bjob_city%5D=Montr%C3%A9al

[enviroemplois.org]
# Multiple start URLs crawl
start_urls=["https://www.enviroemplois.org/offres-d-emploi?sector=&region=6&job_kind=&employer=",
    "https://www.enviroemplois.org/offres-d-emploi?sector=&region=3&job_kind=&employer="]

```

### Run it
```bash
python3 -m alt_job -c /home/user/Jobs/alt_job.conf
```

### Arguments
Some of the config options can be overwritten with CLI arguments.

```
  -c <File path> [<File path> ...], --config_file <File path> [<File path> ...]
                        configuration file(s). Default locations will be
                        checked and loaded if file exists:
                        `~/.alt_job/alt_job.conf`, `~/alt_job.conf` or
                        `./alt_job.conf` (default: [])
  -t, --template_conf   print a template config file and exit. (default:
                        False)
  -V, --version         print Alt Job version and exit. (default: False)
  -x <File path>, --xlsx_output <File path>
                        Write all NEW jobs to Excel file (default: None)
  -s <Website> [<Website> ...], --enabled_scrapers <Website> [<Website> ...]
                        List of enabled scrapers. By default it's all scrapers
                        configured in config file(s) (default: [])
  -j <File path>, --jobs_datafile <File path>
                        JSON file to store ALL jobs data. Default is
                        '~/jobs.json'. Use 'null' keyword to disable the
                        storage of the datafile, all jobs will be considered
                        as new and will be loaded (default: )
  --workers <Number>    Number of websites to scrape asynchronously (default:
                        5)
  --full, --load_all_jobs
                        Load the full job description page to parse
                        additionnal data. This settings is applied to all
                        scrapers (default: False)
  --all, --load_all_new_pages
                        Load new job listing pages until older jobs are found.
                        This settings is applied to all scrapers (default:
                        False)
  --quick, --no_load_all_jobs
                        Do not load the full job description page to parse
                        additionnal data (Much more faster). This settings is
                        applied to all scrapers (default: False)
  --first, --no_load_all_new_pages
                        Load only the first job listing page. This settings is
                        applied to all scrapers (default: False)
  --mailto <Email> [<Email> ...]
                        Emails to notify of new job postings (default: [])
  --log_level <String>  Alt job log level. Exemple: DEBUG (default: INFO)
  --scrapy_log_level <String>
                        Scrapy log level. Exemple: DEBUG (default: ERROR)

```
