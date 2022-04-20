#include "parse.h"

static void parseParameter(xmlDocPtr doc, xmlNode *cur_node)
{
    char *element;
    char *must = NULL;

    if (parameter_count >= parameter_array_size)
    {
        exit(4);
    }
    while (cur_node != NULL)
    {
        printf("%d %d\n", parameter[parameter_count].count,  variable_array_size);
        if (parameter[parameter_count].count >= variable_array_size)
        {
            exit(3);
        }

        if ((!xmlStrcmp(cur_node->name, (const xmlChar *)"MUST")))
        {
            must = ((char *)(xmlNodeListGetString(doc, cur_node->xmlChildrenNode, 1)));
            if (strcmp("true", must) == 0)
            {
                parameter[parameter_count].must = 1;
            }
            else if (strcmp("false", must) == 0)
            {
                parameter[parameter_count].must = 0;
            }
        }
        else if ((!xmlStrcmp(cur_node->name, (const xmlChar *)"ELEMENT")))
        {
            element = ((char *)(xmlNodeListGetString(doc, cur_node->xmlChildrenNode, 1)));

            if (strlen(element) < parameter_strings_long)
            {
                int p = parameter[parameter_count].count;
                strncpy(parameter[parameter_count].parameter[p], element, strlen(element));
            }
            else
            {
                exit(2);
            }

            parameter[parameter_count].count++;
        }
        else if ((!xmlStrcmp(cur_node->name, (const xmlChar *)"text")))
        {
        }
        cur_node = cur_node->next;
    }
    parameter_count++;
}

static void
parseArgvParameter(xmlDocPtr doc, xmlNode *cur_node)
{
    char *element;
    origin_argc = 0;
    origin_argv = (char**)malloc(sizeof(char*) * 200);
    for(int i = 0; i < 200; i++)
        origin_argv[i] = (char*)malloc(sizeof(char) * 200);
        
    while (cur_node != NULL)
    {
        if ((!xmlStrcmp(cur_node->name, (const xmlChar *)"ELEMENT")))
        {
            element = ((char *)(xmlNodeListGetString(doc, cur_node->xmlChildrenNode, 1)));
            char* substr = NULL;
            printf("%s\n", element);
            substr = strtok(element, " ");
            while(substr != NULL) {
                sprintf(origin_argv[origin_argc], "%s", substr);
                origin_argv[origin_argc][strlen(substr)] = '\0';
                origin_argc ++;
                substr = strtok(NULL, " ");
            }
            origin_argv[origin_argc++] = NULL;
        }
        cur_node = cur_node->next;
    }
}


static void
parseRoot(xmlDocPtr doc, xmlNode *a_node)
{
    a_node = a_node->children;
    xmlNode *cur_node = NULL;

    for (cur_node = a_node; cur_node; cur_node = cur_node->next)
    {

        if (!(xmlStrcmp(cur_node->name, (const xmlChar *)"PARAMETER")))
        {
            parseParameter(doc, cur_node->xmlChildrenNode);
        }
        else if (!(xmlStrcmp(cur_node->name, (const xmlChar *)"ARGV")))
        {
            parseArgvParameter(doc, cur_node->xmlChildrenNode);
        }
        else if (!(xmlStrcmp(cur_node->name, (const xmlChar *)"text")))
        {
        }
    }
    return;
}

void print_parse_result()
{
    int i, j;
    printf("parameter :\n");
    for (i = 0; i < parameter_count; i++)
    {
        printf("must = %d,count = %d\n", parameter[i].must, parameter[i].count);
        for (j = 0; j < parameter[i].count; j++)
        {
            printf("%s\n", parameter[i].parameter[j]);
        }
    }
    printf("parameter count = %d\n", parameter_count);
    printf("file:\n%s:\n", file_parameter);
}

void parse_xml(char *xml_posion)
{
    xmlDoc *doc = NULL;
    xmlNode *root_element = NULL;

    LIBXML_TEST_VERSION

    /*parse the file and get the DOM */
    doc = xmlReadFile(xml_posion, NULL, 0);

    if (doc == NULL)
    {
        printf("error: could not parse file %s\n", xml_posion);
    }
    /*Get the root element node */
    root_element = xmlDocGetRootElement(doc);

    parseRoot(doc, root_element);

    xmlFreeDoc(doc);
    xmlCleanupParser();
    print_parse_result();
}
