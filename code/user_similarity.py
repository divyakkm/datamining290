from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol
from itertools import combinations

class UserSimilarity(MRJob):
    INPUT_PROTOCOL = JSONValueProtocol

    # Function to extract and generate user id and business id from reviews
    def extract(self, _, record):
        """Extract the user id and business id from reviews"""
        if record['type'] == 'review':
            yield record["user_id"], record['business_id']

    # Function to generate businessids for each user
    def merge(self, usr_id, biz_id):
        """Generate businessids for each user"""
        yield usr_id, list(set(biz_id))

    # Function to generate key-value pair to be used by mapper later. 'ALL' is a constant
    def distribute(self, usr_id, biz_id):
        yield 'ALL', [usr_id, biz_id]

    # Function to calculate similarity
    def similarity(self, _, usr_biz_pairs):
        """Function to calculate Jaccard's similarity"""
        # print type(usr_biz_pairs)
        for (usr_a, biz_a), (usr_b, biz_b) in combinations(usr_biz_pairs, r=2):
            jaccardsimilarity = UserSimilarity.jaccardCalc(biz_a, biz_b)
            if jaccardsimilarity >= 0.5: #Checking for condition >=0.5
                yield [usr_a, usr_b], jaccardsimilarity

    # Static method to calculate Jaccard's coefficient
    @staticmethod
    def jaccardCalc(a, b):
        """    # Static method to calculate Jaccard's coefficient"""
        return float(len(set(a) & set(b))) / len(set(a) | set(b)) # |Intersection|/|Union|

    # mrjob steps
    def steps(self):
        return [
        self.mr(mapper=self.extract, reducer=self.merge),
        self.mr(mapper=self.distribute, reducer=self.similarity)
        ]


if __name__ == '__main__':
    UserSimilarity.run()
