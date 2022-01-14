import logging
import time
from datetime import datetime

from instagram.lib.InstagramBase import InstagramBase
from instagram.lib.instagram_profile import InstagramProfile
import instagram.model.pb.instagram_profile_relation_pb2 as relation_proto
from kafka.producer import ProtoProducer
from utils.proto import Proto


class InstagramUser(InstagramBase):
    def __init__(self):
        super(InstagramUser, self).__init__()
        self.__instagram_profile = InstagramProfile()
        self.__logger = logging.Logger(__name__)
        self.__relation_producer = ProtoProducer(self.get_profile_collection_key(postfix='relation'),
                                                 relation_proto.InstagramRelationDTO)

    def get_users_to_crawl(self):
        # get to_user in instagram_relation where user is not in from_user
        # from_user contains all users that had been crawled and should be scheduled with more delay.
        # we can crawl users with threshold. for example if followers of a user have been increased more than
        # a threshold, we can schedule it for crawl.
        pass

    def crawl(self, start_username, max_depth: int = 1, current_depth: int = 1):
        profile = self.get_profile(start_username)
        similar_accounts = profile.get_similar_accounts()
        idx = 0
        for acc in similar_accounts:
            self.__instagram_profile.insert_from_profile(acc)
            relation = relation_proto.InstagramRelationDTO(
                from_username=start_username,
                to_username=acc.username,
                relation_type='similar_account',
                created_at=Proto.get_current_timestamp()
            )
            self.__relation_producer.produce(f'{start_username}__{acc.username}_similaracc', relation)
            idx += 1
            if idx % 10 == 0:
                self.__logger.info(f"{idx} similar account detected. Sleep for 30s.")
                time.sleep(30)

        self.__logger.info(f"Finished. Totally {idx} similar account detected.")
        idx = 0
        followees = profile.get_followees()
        for f in followees:
            self.__instagram_profile.insert_from_profile(f)
            relation = relation_proto.InstagramRelationDTO(
                from_username=start_username,
                to_username=f.username,
                relation_type='followee',
                created_at=Proto.get_current_timestamp()
            )
            self.__relation_producer.produce(f'{start_username}__{f.username}_followee', relation)
            idx += 1
            if idx % 10 == 0:
                self.__logger.info(f"{idx} followees detected. Sleep for 30s.")
                time.sleep(30)

        self.__logger.info(f"Finished. Totally {idx} followees detected.")
        followers = profile.get_followers()
        for f in followers:
            self.__instagram_profile.insert_from_profile(f)
            relation = relation_proto.InstagramRelationDTO(
                from_username=start_username,
                to_username=f.username,
                relation_type='follower',
                created_at=Proto.get_current_timestamp()
            )
            self.__relation_producer.produce(f'{start_username}__{f.username}_follower', relation)
            idx += 1
            if idx % 10 == 0:
                self.__logger.info(f"{idx} followers detected. Sleep for 30s.")
                time.sleep(30)
        self.__logger.info(f"Finished {idx} followers detected.")
