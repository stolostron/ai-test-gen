package create_cluster

import (
	"github.com/onsi/ginkgo/v2"
	"github.com/onsi/gomega"

	"k8s.io/klog"

	libgoclusters "github.com/stolostron/acmqe-go-library/pkg/clusters"
)

var _ = ginkgo.Describe("create cluster", ginkgo.Label("create"), func() {

	ginkgo.It("RHACM4K-46697: CLC: Create an AWS managed cluster via ClusterDeployment", ginkgo.Label("aws"), func() {
		clusterName, err := libgoclusters.GetClusterName("aws")
		gomega.Expect(err).NotTo(gomega.HaveOccurred())
		err = Appliers.CreateCluster(clusterName, "aws", "OpenShift")
		if err != nil {
			klog.Error(err)
		}
	})

	ginkgo.It("RHACM4K-46699: CLC: Create an GCP managed cluster via ClusterDeployment", ginkgo.Label("gcp"), func() {
		clusterName, err := libgoclusters.GetClusterName("gcp")
		gomega.Expect(err).NotTo(gomega.HaveOccurred())
		err = Appliers.CreateCluster(clusterName, "gcp", "OpenShift")
		if err != nil {
			klog.Error(err)
		}
	})

	ginkgo.It("RHACM4K-46698: CLC: Create an Azure managed cluster via ClusterDeployment", ginkgo.Label("azure"), func() {
		clusterName, err := libgoclusters.GetClusterName("azure")
		gomega.Expect(err).NotTo(gomega.HaveOccurred())
		err = Appliers.CreateCluster(clusterName, "azure", "OpenShift")
		if err != nil {
			klog.Error(err)
		}
	})

	ginkgo.It("RHACM4K-46700: CLC: Create an Azure Government managed cluster via ClusterDeployment", ginkgo.Label("azgov"), func() {
		clusterName, err := libgoclusters.GetClusterName("azgov")
		gomega.Expect(err).NotTo(gomega.HaveOccurred())
		err = Appliers.CreateCluster(clusterName, "azgov", "OpenShift")
		if err != nil {
			klog.Error(err)
		}
	})

	ginkgo.It("RHACM4K-46701: CLC Create an Openstack managed cluster via ClusterDeployment", ginkgo.Label("openstack"), func() {
		clusterName, err := libgoclusters.GetClusterName("openstack")
		gomega.Expect(err).NotTo(gomega.HaveOccurred())
		err = Appliers.CreateCluster(clusterName, "openstack", "OpenShift")
		if err != nil {
			klog.Error(err)
		}
	})
})
