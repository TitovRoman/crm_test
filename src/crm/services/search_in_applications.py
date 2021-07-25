import datetime
from abc import ABC, abstractmethod
from enum import Enum
import operator
from typing import Optional, Any

from django.db.models import Q
from django.http import QueryDict


class SearchNode(ABC):
    @abstractmethod
    def get_query(self) -> Q:
        pass


class EmptyNode(SearchNode):
    def get_query(self) -> Q:
        return Q()


class SearchOperator(Enum):
    gte = 'gte'
    lte = 'lte'

    in_ = 'in'


class SearchOperatorNode(SearchNode):
    def __init__(self, operator: SearchOperator):
        super().__init__()
        self.search_operator: SearchOperator = operator

    def get_query(self) -> Q:
        query_params = {
            self._get_search_field_name() + '__' + self.search_operator.value:
                self._get_search_value()
        }
        return Q(**query_params)

    @abstractmethod
    def _get_search_field_name(self) -> str:
        pass

    @abstractmethod
    def _get_search_value(self):
        pass


class DateNode(SearchOperatorNode):
    def __init__(self, operator: SearchOperator, date: datetime.date):
        super().__init__(operator)
        self._date: datetime.date = date

    def _get_search_field_name(self) -> str:
        return 'creation_date__date'

    def _get_search_value(self) -> datetime.date:
        return self._date


class DateGteNode(DateNode):
    def __init__(self, date_from: datetime.date):
        super().__init__(SearchOperator.gte, date_from)


class DateLteNode(DateNode):
    def __init__(self, date_to: datetime.date):
        super().__init__(SearchOperator.lte, date_to)


class SearchInListNode(SearchNode):
    def __init__(self, id_list: int):
        self.id_list = id_list

    def get_query(self) -> Q:
        query_params = {self._get_search_field_name() + '__in': self.id_list}
        return Q(**query_params)

    @abstractmethod
    def _get_search_field_name(self) -> str:
        pass


class CategoryIdInListNode(SearchInListNode):
    def _get_search_field_name(self) -> str:
        return 'category__id'


class StatusIdInListNode(SearchInListNode):
    def _get_search_field_name(self) -> str:
        return 'status__id'


class LogicalOperator(Enum):
    AND = operator.and_
    OR = operator.or_


class LogicalOperationNode(SearchNode):
    def __init__(
            self,
            operation: LogicalOperator,
            left: SearchNode,
            right: SearchNode
    ):
        self._operation = operation
        self._left: SearchNode = left
        self._right: SearchNode = right

    def get_query(self) -> Q:
        return self._operation.value(
            self._left.get_query(),
            self._right.get_query()
        )


class SearchInApplicationsParser:
    def __init__(self, search_parameters: dict):
        self.search_parameters = search_parameters

    def _parse_search_parameters(self) -> SearchNode:
        date_node = self._parse_date()
        category_node = self._parse_category()
        status_node = self._parse_status()

        search_node = self._intersection_nodes(
            date_node,
            category_node,
            status_node
        )

        return search_node

    def _get_parameter(self, parameter_name: str) -> Any:
        return self.search_parameters.get(parameter_name)

    def _intersection_nodes(self, *nodes: SearchNode) -> SearchNode:
        result_node = EmptyNode()
        for node in nodes:
            if not isinstance(node, EmptyNode):
                if isinstance(result_node, EmptyNode):
                    result_node = node
                else:
                    result_node = LogicalOperationNode(
                        LogicalOperator.AND,
                        result_node,
                        node
                    )
        return result_node

    def _parse_date(self):
        date_from = self._get_parameter('date_from')
        date_to = self._get_parameter('date_to')

        date_node = EmptyNode()
        if date_from:
            date_node = DateGteNode(date_from)
        if date_to:
            date_node = self._intersection_nodes(
                date_node,
                DateLteNode(date_to)
            )
        return date_node

    def _parse_category(self):
        if application_category := self._get_parameter('application_category'):
            return CategoryIdInListNode(application_category)
        else:
            return EmptyNode()

    def _parse_status(self):
        if application_status := self._get_parameter('application_status'):
            return StatusIdInListNode(application_status)
        else:
            return EmptyNode()


class SearchInApplicationsHandler:
    def __init__(self, search_parameters: dict):
        self.base_search_node: SearchNode = \
            SearchInApplicationsParser(search_parameters)\
                ._parse_search_parameters()

    def get_query(self) -> Q:
        return self.base_search_node.get_query()
