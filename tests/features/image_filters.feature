Feature: Image Filters

  Scenario Outline: Image Filters
    Given an image
    And a loaded <filter> filter
    And a result creator <filter>
    When Applying the filter on the image
    Then The result should be equal to the result of the <result_creator>
    Examples:
      | filter        |
      | gaussian_blur |
      | rotate_image  |
      | brightness    |
      | box filter    |

    Scenario
