from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol

import re
WORD_RE = re.compile(r"[\w']+")

class UniqueReview(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol

    def extract_words(self, _, record):
        """Take in a record, yield <word, review_id>"""
        if record['type'] == 'review':
            for word in WORD_RE.findall(record['text']):
                yield [word.lower(), record['review_id']]

    def count_reviews(self, word, review_ids):
        """Count the number of reviews a word has appeared in.  If it is a
        unique word (ie it has only been used in 1 review), output that review
        and 1 (the number of words that were unique)."""

        unique_reviews = list(set(review_ids))  # set() uniques an iterator
        if len(unique_reviews) == 1:
            yield [unique_reviews.pop(), 1]


    def count_unique_words(self, review_id, unique_word_counts):
        """Output the number of unique words for a given review_id"""
        yield [review_id, sum(unique_word_counts)]


    def aggregate_max(self, review_id, unique_word_count):
        """Group reviews/counts together by the MAX statistic."""
        yield ['MAX', [unique_word_count, review_id]]


    def select_max(self, stat, count_review_ids):
        """Given a list of pairs: [count, review_id], select on the pair with
        the maximum count, and output the result."""
        yield[stat, max(count_review_ids)]

    def steps(self):
        return [
            self.mr(self.extract_words, self.count_reviews),
            self.mr(reducer=self.count_unique_words),
            self.mr(self.aggregate_max, self.select_max),
        ]

if __name__ == '__main__':
    UniqueReview.run()


"""
OUTPUT for all dataset
--------------
"MAX"   [40, "I7lOTTYxHkjc144oAoL0-w"]

"""
