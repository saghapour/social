from datetime import datetime
from instaloader import Profile

from kafka.producer import ProtoProducer
from .InstagramBase import InstagramBase
from database.messages import Messages
from model.result import OperationResult
from utils.cleansing import clean_text
import instagram.model.pb.instagram_profile_pb2 as profile_proto
import instagram.model.pb.instagram_profile_history_pb2 as profile_history_proto
from utils.proto import Proto


class InstagramProfile(InstagramBase):
    def __init__(self):
        super(InstagramProfile, self).__init__()
        self.__profile_producer = ProtoProducer(self.get_profile_collection_key(), profile_proto.InstagramProfileDTO)
        self.__profile_history_producer = ProtoProducer(self.get_profile_collection_key(postfix='history'),
                                                        profile_history_proto.InstagramProfileHistoryDTO)

    def insert_batch(self, usernames: list) -> list:
        exceptions = []
        for username in usernames:
            result = self.insert_from_username(username)
            if result.has_error:
                exceptions.append(username)

        return exceptions

    def insert_from_username(self, username: str, return_object: bool = False) -> OperationResult:
        profile = self.get_profile(username)
        return self.__insert(profile, return_object)

    def insert_from_profile(self, profile: Profile, return_object: bool = False) -> OperationResult:
        return self.__insert(profile, return_object)

    def update_history(self, username: str) -> OperationResult:
        # update profile only change log(time series collection) for profile.
        profile = self.get_profile(username)
        result = OperationResult.get_instance()
        try:
            self.add_profile_history(profile.userid, profile.username, profile.followees, profile.followers,
                                     profile.mediacount)
            result.set_success(Messages.get_success_message())
        except Exception as ex:
            result.set_error(str(ex))
        return result

    def add_profile_history(self, userid, username,
                            total_followees, total_followers,
                            media_count):
        history_dto = profile_history_proto.InstagramProfileHistoryDTO(
            profile_spec={'userid': str(userid), 'username': username},
            total_followees=total_followees,
            total_followers=total_followers,
            media_count=media_count,
            updated_at=Proto.get_current_timestamp()
        )

        self.__profile_history_producer.produce(str(userid), history_dto)

    def __insert(self, profile: Profile, return_object: bool = False) -> OperationResult:
        result = OperationResult.get_instance()
        userid = profile.userid
        dto = profile_proto.InstagramProfileDTO(
            _id=userid,
            userid=userid,
            username=profile.username,
            fullname=clean_text(profile.full_name),
            biography=clean_text(profile.biography),
            external_url=profile.external_url,
            business_category_name=profile.business_category_name,
            is_business_account=profile.is_business_account,
            is_private=profile.is_private,
            # profile_pic_url=profile.profile_pic_url,
            total_followers=profile.followers,
            total_followees=profile.followees,
            media_count=profile.mediacount,
            updated_at=Proto.get_current_timestamp(),
            created_at=Proto.get_current_timestamp()
        )

        try:
            self.__profile_producer.produce(str(userid), dto)
            self.add_profile_history(dto.userid, dto.username,
                                     dto.total_followees, dto.total_followers, dto.media_count)

            if return_object:
                result.set_object(dto)
            result.set_success(Messages.get_success_message())
        except Exception as ex:
            result.set_error(str(ex))

        return result
