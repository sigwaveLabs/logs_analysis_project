#!/usr/bin/env python2

from datetime import datetime
import psycopg2


def connect(database_name="news"):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        c = db.cursor()
        print "Successfully connected to the '%s' database." % database_name
        return db, c
    except psycopg2.Error:
        print "Unable to connect to database '%s' database." % database_name
        exit(1)


def get_query_results(query, c):
    """Runs db query, pass in query string and cursor"""
    c.execute(query)
    results = c.fetchall()
    return results


def get_top_articles(c):
    """Returns string of the top three most viewed articles"""
    s = "\nThe top three most viewed articles are:\n"
    query = "select * from article_views limit 3;"
    results = get_query_results(query, c)
    for row in results:
        s += " * " + "\"" + str(row[0]) + "\" -- " + str(row[1]) + " views\n"
    return s


def get_top_authors(c):
    """Returns string of the top three most popular authors"""
    s = "\nThe top three most popular authors are:\n"
    query = "select * from author_views limit 3;"
    results = get_query_results(query, c)
    for row in results:
        s += " * " + str(row[0]) + " -- " + str(row[1]) + " views\n"
    return s


def get_view_errors(c):
    """Returns string of the percentage of article request errors"""
    s = "\nThe days where more than 1% of requests led to errors are:\n"
    query = "select * from error_percent where error_percent > 1;"
    results = get_query_results(query, c)
    for row in results:
        s += " * " + str(row[0]) + " -- " + str(row[1]) + "% errors\n"
    return s


def print_to_file(file_name, text):
    """Print the report to a plain text file"""
    f = open(file_name, "w")
    f.write(text)
    f.close()


def get_report(date, c):
    """Returns string of report"""
    report = ""
    report = "\nAs of " + date + ":\n"
    report += get_top_articles(c)
    report += get_top_authors(c)
    report += get_view_errors(c)
    return report


def main():
    """Main function, open db connection, get the current datetime,
    build the report, printsreport to the terminal, print report to text file,
    colse db connection and print status"""
    db, c = connect()  # connect to database
    date = datetime.now().strftime('%Y-%m-%d %H:%M')  # get current datetime
    report = get_report(date, c)  # build the report
    print report  # print report to terminal
    print_to_file("log_reports/log_report_" + date, report)  # print report
    db.close()  # close db connection
    print "Report created successfully :)"


if __name__ == '__main__':
    main()
