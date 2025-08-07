package import_cluster

import (
	"context"
	"fmt"
	"os"
	"path/filepath"
	"strings"

	"github.com/onsi/ginkgo/v2"
	"github.com/onsi/gomega"
	v1 "k8s.io/apimachinery/pkg/apis/meta/v1"

	"github.com/stolostron/acmqe-go-library/pkg/clusters"
)

var _ = ginkgo.Describe("import cluster", ginkgo.Label("import"), func() {
	ginkgo.It("RHACM4K-46708: CLC: Import IKS cluster via AutoImportSecret and API Token", ginkgo.Label("iks", "token"), func() {
		kubeConfig, clusterName, err := getKubeConfig("*-iks-ibmapi.kubeconfig")
		gomega.Expect(err).ShouldNot(gomega.HaveOccurred())
		err = Appliers.ImportCluster(clusterName, "iks", "token", kubeConfig)
		gomega.Expect(err).ShouldNot(gomega.HaveOccurred())
	})

	ginkgo.It("RHACM4K-46707: CLC: Import IKS cluster via AutoImportSecret and Kubeconfig", ginkgo.Label("iks", "kubeconfig"), func() {
		kubeConfig, clusterName, err := getKubeConfig("*-iks.kubeconfig")
		gomega.Expect(err).ShouldNot(gomega.HaveOccurred())
		err = Appliers.ImportCluster(clusterName, "iks", "kubeconfig", kubeConfig)
		gomega.Expect(err).ShouldNot(gomega.HaveOccurred())
	})

	ginkgo.It("RHACM4K-46710: CLC: Import EKS cluster via AutoImportSecret and API Token", ginkgo.Label("eks", "token"), func() {
		kubeConfig, clusterName, err := getKubeConfig("*-eks.kubeconfig")
		gomega.Expect(err).ShouldNot(gomega.HaveOccurred())
		err = Appliers.ImportCluster(clusterName, "eks", "token", kubeConfig)
		gomega.Expect(err).ShouldNot(gomega.HaveOccurred())
	})

	ginkgo.It("RHACM4K-46709: CLC: Import EKS cluster via AutoImportSecret and Kubeconfig", ginkgo.Label("eks", "kubeconfig"), func() {
		kubeConfig, clusterName, err := getKubeConfig("*-eks.kubeconfig")
		gomega.Expect(err).ShouldNot(gomega.HaveOccurred())
		err = Appliers.ImportCluster(clusterName, "eks", "kubeconfig", kubeConfig)
		gomega.Expect(err).ShouldNot(gomega.HaveOccurred())
	})

	ginkgo.It("RHACM4K-46712: CLC: Import GKE cluster via AutoImportSecret and API Token", ginkgo.Label("gke", "token"), func() {
		kubeConfig, clusterName, err := getKubeConfig("*-gcp.kubeconfig")
		gomega.Expect(err).ShouldNot(gomega.HaveOccurred())
		err = Appliers.ImportCluster(clusterName, "gke", "token", kubeConfig)
		gomega.Expect(err).ShouldNot(gomega.HaveOccurred())
	})

	ginkgo.It("RHACM4K-46711: CLC: Import GKE cluster via AutoImportSecret and Kubeconfig", ginkgo.Label("gke", "kubeconfig"), func() {
		kubeConfig, clusterName, err := getKubeConfig("*-gcp.kubeconfig")
		gomega.Expect(err).ShouldNot(gomega.HaveOccurred())
		err = Appliers.ImportCluster(clusterName, "gke", "kubeconfig", kubeConfig)
		gomega.Expect(err).ShouldNot(gomega.HaveOccurred())
	})

	ginkgo.It("RHACM4K-46713: CLC: Import AKS cluster via AutoImportSecret and API Token", ginkgo.Label("aks", "token"), func() {
		kubeConfig, clusterName, err := getKubeConfig("*-aks.kubeconfig")
		gomega.Expect(err).ShouldNot(gomega.HaveOccurred())
		err = Appliers.ImportCluster(clusterName, "aks", "token", kubeConfig)
		gomega.Expect(err).ShouldNot(gomega.HaveOccurred())
	})

	ginkgo.It("RHACM4K-46714: CLC: Import AKS cluster via AutoImportSecret and Kubeconfig", ginkgo.Label("aks", "kubeconfig"), func() {
		kubeConfig, clusterName, err := getKubeConfig("*-aks.kubeconfig")
		gomega.Expect(err).ShouldNot(gomega.HaveOccurred())
		err = Appliers.ImportCluster(clusterName, "aks", "kubeconfig", kubeConfig)
		gomega.Expect(err).ShouldNot(gomega.HaveOccurred())
	})

	ginkgo.It("RHACM4K-46716: CLC: Import ROKS cluster via AutoImportSecret and API Token", ginkgo.Label("roks", "token"), func() {
		kubeConfig, clusterName, err := getKubeConfig("*-roks-ibmapi.kubeconfig")
		gomega.Expect(err).ShouldNot(gomega.HaveOccurred())
		err = Appliers.ImportCluster(clusterName, "roks", "token", kubeConfig)
		gomega.Expect(err).ShouldNot(gomega.HaveOccurred())
	})

	ginkgo.It("RHACM4K-46715: CLC: Import ROKS cluster via AutoImportSecret and Kubeconfig", ginkgo.Label("roks", "kubeconfig"), func() {
		kubeConfig, clusterName, err := getKubeConfig("*-roks.kubeconfig")
		gomega.Expect(err).ShouldNot(gomega.HaveOccurred())
		err = Appliers.ImportCluster(clusterName, "roks", "kubeconfig", kubeConfig)
		gomega.Expect(err).ShouldNot(gomega.HaveOccurred())
	})

	ginkgo.It("RHACM4K-46720: CLC: Import ROSA Classic cluster via AutoImportSecret and API Token", ginkgo.Label("rosa-classic", "token"), func() {
		kubeConfig, clusterName, err := getKubeConfig("*-rosa.kubeconfig")
		gomega.Expect(err).ShouldNot(gomega.HaveOccurred())
		err = Appliers.ImportCluster(clusterName, "rosa", "token", kubeConfig)
		gomega.Expect(err).ShouldNot(gomega.HaveOccurred())
	})

	ginkgo.It("RHACM4K-46718: CLC: Import ROSA Classic cluster via AutoImportSecret and Kubeconfig", ginkgo.Label("rosa-classic", "kubeconfig"), func() {
		kubeConfig, clusterName, err := getKubeConfig("*-rosa.kubeconfig")
		gomega.Expect(err).ShouldNot(gomega.HaveOccurred())
		err = Appliers.ImportCluster(clusterName, "rosa", "kubeconfig", kubeConfig)
		gomega.Expect(err).ShouldNot(gomega.HaveOccurred())
	})

	ginkgo.It("RHACM4K-46723: CLC: Import ARO cluster via AutoImportSecret and API Token", ginkgo.Label("aro", "token"), func() {
		kubeConfig, clusterName, err := getKubeConfig("*-aro.kubeconfig")
		gomega.Expect(err).ShouldNot(gomega.HaveOccurred())
		err = Appliers.ImportCluster(clusterName, "aro", "token", kubeConfig)
		gomega.Expect(err).ShouldNot(gomega.HaveOccurred())
	})

	ginkgo.It("RHACM4K-46724: CLC: Import ARO cluster via AutoImportSecret and Kubeconfig", ginkgo.Label("aro", "kubeconfig"), func() {
		kubeConfig, clusterName, err := getKubeConfig("*-aro.kubeconfig")
		gomega.Expect(err).ShouldNot(gomega.HaveOccurred())
		err = Appliers.ImportCluster(clusterName, "aro", "kubeconfig", kubeConfig)
		gomega.Expect(err).ShouldNot(gomega.HaveOccurred())
	})

	ginkgo.It("RHACM4K-46722: CLC: Import OCP3 cluster via AutoImportSecret and API Token", ginkgo.Label("ocp311", "token"), func() {
		kubeConfig, clusterName, err := getKubeConfig("*-ocp311.kubeconfig")
		gomega.Expect(err).ShouldNot(gomega.HaveOccurred())
		err = Appliers.ImportCluster(clusterName, "ocp311", "token", kubeConfig)
		gomega.Expect(err).ShouldNot(gomega.HaveOccurred())
	})

	ginkgo.It("RHACM4K-46717: CLC: Import OCP3 cluster via AutoImportSecret and Kubeconfig", ginkgo.Label("ocp311", "kubeconfig"), func() {
		kubeConfig, clusterName, err := getKubeConfig("*-ocp311.kubeconfig")
		gomega.Expect(err).ShouldNot(gomega.HaveOccurred())
		err = Appliers.ImportCluster(clusterName, "ocp311", "kubeconfig", kubeConfig)
		gomega.Expect(err).ShouldNot(gomega.HaveOccurred())
	})

	ginkgo.It("RHACM4K-46719: CLC: Import ROSA HCP cluster via AutoImportSecret and Kubeconfig", ginkgo.Label("rosa-hcp", "kubeconfig"), func() {
		kubeConfig, clusterName, err := getKubeConfig("*-rosa-hcp.kubeconfig")
		gomega.Expect(err).ShouldNot(gomega.HaveOccurred())
		err = Appliers.ImportCluster(clusterName, "rosa-hcp", "kubeconfig", kubeConfig)
		gomega.Expect(err).ShouldNot(gomega.HaveOccurred())

		// Check cluster claim
		importedCluster, err := Appliers.ClusterClient.ClusterV1().ManagedClusters().Get(context.TODO(), clusterName, v1.GetOptions{})
		gomega.Expect(err).ShouldNot(gomega.HaveOccurred())
		for _, clusterClaim := range importedCluster.Status.ClusterClaims {
			switch clusterClaim.Name {
			case "platform.open-cluster-management.io":
				gomega.Expect(clusterClaim.Value).Should(gomega.Equal("AWS"))
			case "product.open-cluster-management.io":
				gomega.Expect(clusterClaim.Value).Should(gomega.Equal("ROSA"))
			case "hostedcluster.hypershift.openshift.io":
				gomega.Expect(clusterClaim.Value).Should(gomega.Equal("true"))
			}
		}
	})
})

func getKubeConfig(suffix string) ([]byte, string, error) {
	fileName, _ := clusters.GetFileName("../../resources/clusters", suffix)
	if fileName != nil {
		kubeConfig, err := os.ReadFile(filepath.Clean(fileName[0]))
		if err != nil {
			return nil, "", err
		}
		clusterName := strings.Split(filepath.Base(fileName[0]), ".")[0]
		return kubeConfig, clusterName, nil
	}
	return nil, "", fmt.Errorf("failed to get the file")
}
