from shared_science.models.model_utils import ResourceSQLModel


def has_access_to_resource(email, resource: ResourceSQLModel):
    """Naive implementation of read-access IAM.

    Notes:
        Using something like casbin could be beneficial here.
    """
    return email in resource.user_read_allow.split(",")
