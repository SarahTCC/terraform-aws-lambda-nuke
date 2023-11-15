# -*- coding: utf-8 -*-

"""Module deleting all aws Elastic Container Service resources."""

from typing import Iterator

from botocore.exceptions import EndpointConnectionError

from nuke.client_connections import AwsClient
from nuke.exceptions import ClientError, nuke_exceptions


class NukeEcs:
    """Abstract ecs nuke in a class."""

    def __init__(self, region_name=None) -> None:
        """Initialize ecs nuke."""
        self.ecs = AwsClient().connect("ecs", region_name)

        try:
            self.ecs.list_ecs()
        except EndpointConnectionError:
            print("Ecs resource is not available in this aws region")
            return

    def nuke(self) -> None:
        try:
            self.ecs.list_clusters()
        except EndpointConnectionError:
            print('ecs resource is not available in this aws region')
            return

        # List all ecs cluster
        ecs_cluster_list = self.ecs_list_clusters()

        # Nuke all ecs cluster
        for cluster in ecs_cluster_list:
            try:
                self.ecs.delete_cluster(cluster=cluster)
                print("Nuke ECS cluster{0}".format(cluster))
            except ClientError as exc:
                nuke_exceptions("ecs cluster", cluster, exc)

    def list_registry(self) -> Iterator[str]:
        # Set paginator
        paginator = self.ecs.get_paginator('list_clusters')
        page_iterator = paginator.paginate()

        ecs_cluster_list = []

        # Retrieve all ecs cluster
        for page in page_iterator:
            for cluster in page['clusterArns']:

                ecs_cluster = cluster
                ecs_cluster_list.insert(0, ecs_cluster)

        return ecs_cluster_list
